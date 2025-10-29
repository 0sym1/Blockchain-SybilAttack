"""
Node class - Đại diện cho một node trong mạng P2P blockchain
"""
import json
import uuid
import requests
from flask import Flask, request, jsonify
from threading import Thread
import config
from core.blockchain import Blockchain
from core.transaction import Transaction
from core.block import Block


class Node:
    def __init__(self, host='127.0.0.1', port=None, username=None):
        """
        Khởi tạo node
        
        Args:
            host (str): Host address
            port (int): Port number
            username (str): Tên người dùng
        """
        self.node_id = str(uuid.uuid4())
        self.host = host
        self.port = port or self.find_available_port()
        self.username = username or f"Node_{self.port}"
        
        # Blockchain của node với initial balance cho owner
        self.blockchain = Blockchain(owner_address=self.username)
        
        # Danh sách peers (node_id -> url)
        self.peers = {}
        
        # Flask app cho API
        self.app = Flask(__name__)
        self.setup_routes()
        
        # Server thread
        self.server_thread = None
    
    def find_available_port(self):
        """
        Tìm port khả dụng
        
        Returns:
            int: Port number
        """
        import socket
        base_port = config.BASE_PORT
        
        for port in range(base_port, base_port + 1000):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('127.0.0.1', port))
                    return port
                except:
                    continue
        
        raise Exception("No available port found!")
    
    def setup_routes(self):
        """Setup Flask API routes"""
        
        @self.app.route('/ping', methods=['GET'])
        def ping():
            """Health check endpoint"""
            return jsonify({'status': 'ok', 'node_id': self.node_id})
        
        @self.app.route('/info', methods=['GET'])
        def info():
            """Lấy thông tin node"""
            return jsonify({
                'node_id': self.node_id,
                'username': self.username,
                'host': self.host,
                'port': self.port,
                'chain_length': len(self.blockchain.chain),
                'peers_count': len(self.peers),
                'peers': list(self.peers.keys()),  # Add peer list for debugging
                'pending_transactions': len(self.blockchain.pending_transactions)
            })
        
        @self.app.route('/chain', methods=['GET'])
        def get_chain():
            """Lấy toàn bộ blockchain"""
            return jsonify({
                'chain': self.blockchain.to_list(),
                'length': len(self.blockchain.chain)
            })
        
        @self.app.route('/add_peer', methods=['POST'])
        def add_peer():
            """Thêm peer mới"""
            data = request.get_json()
            peer_id = data.get('peer_id')
            peer_url = data.get('peer_url')
            
            if not peer_id or not peer_url:
                return jsonify({'error': 'Invalid data'}), 400
            
            # Try to add peer (respects MAX_PEERS limit)
            success = self.add_peer(peer_id, peer_url)
            
            if success:
                return jsonify({
                    'message': 'Peer added successfully',
                    'peers_count': len(self.peers)
                })
            else:
                return jsonify({
                    'error': 'Cannot add peer (MAX_PEERS limit reached)',
                    'peers_count': len(self.peers),
                    'max_peers': config.MAX_PEERS
                }), 429  # Too Many Requests
        
        @self.app.route('/remove_peer', methods=['POST'])
        def remove_peer():
            """Xóa peer"""
            data = request.get_json()
            peer_id = data.get('peer_id')
            
            if peer_id:
                self.remove_peer(peer_id)
                return jsonify({'message': 'Peer removed successfully'})
            
            return jsonify({'error': 'Invalid data'}), 400
        
        @self.app.route('/cleanup_peers', methods=['POST'])
        def cleanup_peers():
            """Xóa tất cả peers không còn hoạt động"""
            removed = self.cleanup_stale_peers()
            return jsonify({
                'message': f'Cleaned up {removed} stale peer(s)',
                'removed_count': removed,
                'remaining_peers': len(self.peers)
            })
        
        @self.app.route('/transaction/new', methods=['POST'])
        def new_transaction():
            """Nhận transaction mới từ peer"""
            data = request.get_json()
            
            try:
                transaction = Transaction.from_dict(data)
                
                # Check if transaction already exists in pending
                already_exists = any(
                    tx.sender == transaction.sender and
                    tx.receiver == transaction.receiver and
                    tx.amount == transaction.amount and
                    abs(tx.timestamp - transaction.timestamp) < 1
                    for tx in self.blockchain.pending_transactions
                )
                
                if already_exists:
                    print(f"⚠️ Transaction already in pending pool, skipping")
                    return jsonify({'message': 'Transaction already exists'})
                
                self.blockchain.add_transaction(transaction)
                print(f"✅ Received transaction from peer: {transaction}")
                return jsonify({'message': 'Transaction added successfully'})
            except ValueError as e:
                # Validation error (e.g., insufficient balance)
                print(f"⚠️ Transaction validation failed: {str(e)}")
                return jsonify({'error': str(e)}), 400
            except Exception as e:
                print(f"❌ Error processing transaction: {str(e)}")
                return jsonify({'error': str(e)}), 400
        
        @self.app.route('/block/new', methods=['POST'])
        def new_block():
            """Nhận block mới từ peer"""
            data = request.get_json()
            
            try:
                # Recreate block from dict
                block = Block.from_dict(data)
                
                # Validate block
                if block.previous_hash != self.blockchain.get_latest_block().hash:
                    return jsonify({'error': 'Invalid previous_hash'}), 400
                
                if not block.hash.startswith('0' * self.blockchain.difficulty):
                    return jsonify({'error': 'Invalid proof of work'}), 400
                
                # Add block to chain
                self.blockchain.chain.append(block)
                
                # Remove transaction từ pending nếu có
                if block.transaction:
                    # Tìm và xóa transaction tương tự trong pending
                    self.blockchain.pending_transactions = [
                        tx for tx in self.blockchain.pending_transactions
                        if not (tx.sender == block.transaction.sender and
                                tx.receiver == block.transaction.receiver and
                                tx.amount == block.transaction.amount and
                                abs(tx.timestamp - block.transaction.timestamp) < 1)
                    ]
                
                print(f"✅ Received and added block #{block.index} from peer")
                return jsonify({'message': 'Block added successfully'})
            except Exception as e:
                print(f"❌ Error processing block: {str(e)}")
                return jsonify({'error': str(e)}), 400
        
        @self.app.route('/chain/replace', methods=['POST'])
        def replace_chain():
            """Replace current blockchain with a new one (for Eclipse attack sync)"""
            data = request.get_json()
            
            try:
                new_chain = data.get('chain', [])
                new_length = data.get('length', 0)
                force_replace = data.get('force', False)  # Force replace for sync
                
                if not new_chain or new_length == 0:
                    return jsonify({'error': 'Invalid chain data'}), 400
                
                current_length = len(self.blockchain.chain)
                
                # Only replace if new chain is longer OR force flag is set OR same length
                if new_length < current_length and not force_replace:
                    return jsonify({
                        'message': 'Current chain is longer',
                        'replaced': False,
                        'current_length': current_length,
                        'new_length': new_length
                    })
                
                # Validate and reconstruct chain
                from core.block import Block
                reconstructed_chain = []
                
                for block_data in new_chain:
                    block = Block.from_dict(block_data)
                    reconstructed_chain.append(block)
                
                # Basic validation: check genesis block
                if reconstructed_chain[0].index != 0:
                    return jsonify({'error': 'Invalid genesis block'}), 400
                
                # Replace chain
                self.blockchain.chain = reconstructed_chain
                
                # Clear pending transactions that are already in new chain
                self.blockchain.pending_transactions = []
                
                print(f"✅ Chain replaced! Old: {current_length} blocks → New: {new_length} blocks")
                
                return jsonify({
                    'message': 'Chain replaced successfully',
                    'replaced': True,
                    'old_length': current_length,
                    'new_length': new_length
                })
                
            except Exception as e:
                print(f"❌ Error replacing chain: {str(e)}")
                return jsonify({'error': str(e)}), 400
        
        @self.app.route('/resolve', methods=['POST'])
        def resolve():
            """Đồng bộ blockchain với peers"""
            replaced = self.resolve_conflicts()
            
            if replaced:
                return jsonify({
                    'message': 'Chain was replaced',
                    'new_chain': self.blockchain.to_list()
                })
            else:
                return jsonify({
                    'message': 'Chain is authoritative',
                    'chain': self.blockchain.to_list()
                })
        
        @self.app.route('/sync', methods=['POST'])
        def sync():
            """Alias for /resolve - Đồng bộ blockchain với peers"""
            return resolve()
        
        @self.app.route('/shutdown', methods=['POST'])
        def shutdown():
            """Shutdown Flask server"""
            func = request.environ.get('werkzeug.server.shutdown')
            if func is not None:
                func()
            return jsonify({'message': 'Server shutting down...'})
    
    def start(self):
        """Start node server"""
        print(f"\nStarting node: {self.username}")
        print(f"Node ID: {self.node_id}")
        print(f"URL: http://{self.host}:{self.port}")
        
        self.server_thread = Thread(target=self._run_server, daemon=True)
        self.server_thread.start()
        
        # Đợi server khởi động
        import time
        time.sleep(0.5)
    
    def _run_server(self):
        """Run Flask server"""
        self.app.run(host=self.host, port=self.port, threaded=True, use_reloader=False)
    
    def stop(self):
        """Stop node server"""
        try:
            # Gửi request shutdown đến Flask server
            import requests
            requests.post(f"{self.get_url()}/shutdown", timeout=1)
        except:
            pass  # Server có thể đã dừng rồi
    
    def get_url(self):
        """
        Lấy URL của node
        
        Returns:
            str: URL
        """
        return f"http://{self.host}:{self.port}"
    
    def add_peer(self, peer_id, peer_url):
        """
        Thêm peer (respect MAX_PEERS limit)
        
        Args:
            peer_id (str): ID của peer
            peer_url (str): URL của peer
            
        Returns:
            bool: True if added, False if rejected (max peers reached)
        """
        # Check if already have this peer
        if peer_id == self.node_id:
            return False
        
        if peer_id in self.peers:
            print(f"Peer already exists: {peer_id}")
            return True
        
        # Check MAX_PEERS limit
        if len(self.peers) >= config.MAX_PEERS:
            print(f"❌ Cannot add peer {peer_id}: MAX_PEERS limit reached ({len(self.peers)}/{config.MAX_PEERS})")
            return False
        
        # Add peer
        self.peers[peer_id] = peer_url
        print(f"✓ Peer added: {peer_id} ({peer_url}) [{len(self.peers)}/{config.MAX_PEERS}]")
        return True
    
    def remove_peer(self, peer_id, verbose=True):
        """
        Xóa peer
        
        Args:
            peer_id (str): ID của peer
            verbose (bool): In ra log hay không
        """
        if peer_id in self.peers:
            del self.peers[peer_id]
            if verbose:
                print(f"Peer removed: {peer_id}")
    
    def check_peer_health(self, peer_url, timeout=2):
        """
        Kiểm tra peer còn hoạt động không
        
        Args:
            peer_url (str): URL của peer
            timeout (int): Timeout in seconds
            
        Returns:
            bool: True nếu peer còn sống, False nếu chết
        """
        try:
            import requests
            response = requests.get(f"{peer_url}/info", timeout=timeout)
            return response.status_code == 200
        except:
            return False
    
    def cleanup_stale_peers(self, verbose=True):
        """
        Xóa tất cả peers không còn hoạt động
        
        Args:
            verbose (bool): In ra thông tin chi tiết hay không
        
        Returns:
            int: Số lượng peers đã xóa
        """
        stale_peers = []
        
        # Kiểm tra từng peer
        for peer_id, peer_url in list(self.peers.items()):
            if not self.check_peer_health(peer_url, timeout=1):
                stale_peers.append(peer_id)
        
        # Xóa các stale peers
        for peer_id in stale_peers:
            if verbose:
                print(f"⚠️ Removing stale peer: {peer_id[:8]}... (unreachable)")
            self.remove_peer(peer_id, verbose=False)  # Silent remove
        
        if stale_peers and verbose:
            print(f"✓ Cleaned up {len(stale_peers)} stale peer(s)")
            print(f"  Remaining peers: {len(self.peers)}/{config.MAX_PEERS}")
        
        return len(stale_peers)
    
    def broadcast_transaction(self, transaction, auto_cleanup=False):
        """
        Broadcast transaction đến tất cả peers
        
        Args:
            transaction (Transaction): Transaction cần broadcast
            auto_cleanup (bool): Tự động xóa failed peers (default: False)
        """
        print(f"\nBroadcasting transaction to {len(self.peers)} peers...")
        
        failed_peers = []
        
        for peer_id, peer_url in list(self.peers.items()):
            try:
                response = requests.post(
                    f"{peer_url}/transaction/new",
                    json=transaction.to_dict(),
                    timeout=2
                )
                
                if response.status_code == 200:
                    print(f"✓ Transaction sent to {peer_id[:8]}...")
                else:
                    print(f"✗ Failed to send to {peer_id[:8]}... (HTTP {response.status_code})")
                    failed_peers.append(peer_id)
            except Exception as e:
                print(f"✗ Error sending to {peer_id[:8]}...: {str(e)}")
                failed_peers.append(peer_id)
        
        # Auto cleanup failed peers (optional)
        if failed_peers and auto_cleanup:
            print(f"\n⚠️ Removing {len(failed_peers)} unreachable peer(s)...")
            for peer_id in failed_peers:
                self.remove_peer(peer_id)
            print(f"✓ Remaining peers: {len(self.peers)}/{config.MAX_PEERS}")
    
    def broadcast_block(self, block, auto_cleanup=False):
        """
        Broadcast block đến tất cả peers
        
        Args:
            block (Block): Block cần broadcast
            auto_cleanup (bool): Tự động xóa failed peers (default: False)
        """
        print(f"\nBroadcasting block to {len(self.peers)} peers...")
        
        failed_peers = []
        
        for peer_id, peer_url in list(self.peers.items()):
            try:
                response = requests.post(
                    f"{peer_url}/block/new",
                    json=block.to_dict(),
                    timeout=2
                )
                
                if response.status_code == 200:
                    print(f"✓ Block sent to {peer_id[:8]}...")
                else:
                    print(f"✗ Failed to send to {peer_id[:8]}... (HTTP {response.status_code})")
                    failed_peers.append(peer_id)
            except Exception as e:
                print(f"✗ Error sending to {peer_id[:8]}...: {str(e)}")
                failed_peers.append(peer_id)
        
        # Auto cleanup failed peers (optional)
        if failed_peers and auto_cleanup:
            print(f"\n⚠️ Removing {len(failed_peers)} unreachable peer(s)...")
            for peer_id in failed_peers:
                self.remove_peer(peer_id)
            print(f"✓ Remaining peers: {len(self.peers)}/{config.MAX_PEERS}")
    
    def request_chain(self, peer_url):
        """
        Request blockchain từ peer
        
        Args:
            peer_url (str): URL của peer
        
        Returns:
            list: Blockchain data hoặc None
        """
        try:
            response = requests.get(f"{peer_url}/chain", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return data['chain']
        except Exception as e:
            print(f"Error requesting chain from {peer_url}: {str(e)}")
        
        return None
    
    def resolve_conflicts(self):
        """
        Consensus algorithm - Thay thế chain bằng chain dài nhất từ peers
        
        Returns:
            bool: True nếu chain được thay thế
        """
        longest_chain = None
        max_length = len(self.blockchain.chain)
        
        print("\nResolving conflicts with peers...")
        print(f"Current chain length: {max_length}")
        print(f"Current peers: {len(self.peers)}")
        
        # If no peers, try to discover from network
        if len(self.peers) == 0:
            print("No peers found, discovering from network...")
            try:
                from network.network_manager import NetworkManager
                network_manager = NetworkManager()
                all_nodes = network_manager.get_all_nodes()
                
                # Add network nodes as temporary peers
                for node in all_nodes:
                    if node['node_id'] != self.node_id:
                        peer_url = f"http://{node['host']}:{node['port']}"
                        self.add_peer(node['node_id'], peer_url)
                
                print(f"Discovered {len(self.peers)} peers from network")
            except Exception as e:
                print(f"Failed to discover peers: {str(e)}")
        
        # Check all peers for longer chains
        for peer_id, peer_url in self.peers.items():
            print(f"Checking {peer_id[:8]}... ({peer_url})")
            chain_data = self.request_chain(peer_url)
            
            if chain_data:
                length = len(chain_data)
                print(f"  Peer chain length: {length}")
                
                if length > max_length:
                    max_length = length
                    longest_chain = chain_data
                    print(f"  ✓ Found longer chain! (length: {length})")
        
        if longest_chain:
            if self.blockchain.replace_chain(longest_chain):
                print(f"\n✅ Chain replaced with longer chain! ({len(self.blockchain.chain)} blocks)")
                return True
        
        print("\n✅ Chain is up to date")
        return False
    
    def create_transaction(self, receiver, amount):
        """
        Tạo giao dịch mới
        
        Args:
            receiver (str): Địa chỉ người nhận
            amount (float): Số lượng coin
        
        Returns:
            Transaction: Transaction được tạo (hoặc None nếu insufficient balance)
        
        Raises:
            ValueError: Nếu không đủ balance
        """
        # Validate balance (confirmed + pending để tránh double-spending)
        confirmed = self.blockchain.get_balance(self.username)
        pending = self.blockchain.get_pending_balance(self.username)
        available = confirmed + pending
        
        if available < amount:
            raise ValueError(
                f"Insufficient balance! Available: {available} coins "
                f"(Confirmed: {confirmed}, Pending: {pending})"
            )
        
        transaction = Transaction(
            sender=self.username,
            receiver=receiver,
            amount=amount
        )
        
        # Thêm vào blockchain local
        self.blockchain.add_transaction(transaction)
        
        # Broadcast đến peers
        self.broadcast_transaction(transaction)
        
        return transaction
    
    def mine_block(self):
        """
        Mine block mới
        
        Returns:
            Block: Block được mine (hoặc None)
        """
        block = self.blockchain.mine_pending_transactions(self.username)
        
        if block:
            # Broadcast block đến peers
            self.broadcast_block(block)
        
        return block
    
    def get_balance(self):
        """
        Lấy số dư của node
        
        Returns:
            float: Số dư
        """
        return self.blockchain.get_balance(self.username)
    
    def display_info(self):
        """Hiển thị thông tin node"""
        print("\n" + "="*80)
        print(f"NODE INFORMATION")
        print("="*80)
        print(f"Username: {self.username}")
        print(f"Node ID: {self.node_id}")
        print(f"URL: {self.get_url()}")
        print(f"Balance: {self.get_balance()} coins")
        print(f"Blockchain length: {len(self.blockchain.chain)}")
        print(f"Pending transactions: {len(self.blockchain.pending_transactions)}")
        print(f"Connected peers: {len(self.peers)}")
        
        if self.peers:
            print("\nPeers:")
            for peer_id, peer_url in self.peers.items():
                print(f"  - {peer_id[:8]}... ({peer_url})")
        
        print("="*80 + "\n")
