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
            
            if peer_id and peer_url:
                self.add_peer(peer_id, peer_url)
                return jsonify({'message': 'Peer added successfully'})
            
            return jsonify({'error': 'Invalid data'}), 400
        
        @self.app.route('/remove_peer', methods=['POST'])
        def remove_peer():
            """Xóa peer"""
            data = request.get_json()
            peer_id = data.get('peer_id')
            
            if peer_id:
                self.remove_peer(peer_id)
                return jsonify({'message': 'Peer removed successfully'})
            
            return jsonify({'error': 'Invalid data'}), 400
        
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
        
        @self.app.route('/chain/resolve', methods=['GET'])
        def resolve_chain():
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
        Thêm peer
        
        Args:
            peer_id (str): ID của peer
            peer_url (str): URL của peer
        """
        if peer_id != self.node_id and peer_id not in self.peers:
            self.peers[peer_id] = peer_url
            print(f"Peer added: {peer_id} ({peer_url})")
    
    def remove_peer(self, peer_id):
        """
        Xóa peer
        
        Args:
            peer_id (str): ID của peer
        """
        if peer_id in self.peers:
            del self.peers[peer_id]
            print(f"Peer removed: {peer_id}")
    
    def broadcast_transaction(self, transaction):
        """
        Broadcast transaction đến tất cả peers
        
        Args:
            transaction (Transaction): Transaction cần broadcast
        """
        print(f"\nBroadcasting transaction to {len(self.peers)} peers...")
        
        for peer_id, peer_url in self.peers.items():
            try:
                response = requests.post(
                    f"{peer_url}/transaction/new",
                    json=transaction.to_dict(),
                    timeout=2
                )
                
                if response.status_code == 200:
                    print(f"✓ Transaction sent to {peer_id}")
                else:
                    print(f"✗ Failed to send to {peer_id}")
            except Exception as e:
                print(f"✗ Error sending to {peer_id}: {str(e)}")
    
    def broadcast_block(self, block):
        """
        Broadcast block đến tất cả peers
        
        Args:
            block (Block): Block cần broadcast
        """
        print(f"\nBroadcasting block to {len(self.peers)} peers...")
        
        for peer_id, peer_url in self.peers.items():
            try:
                response = requests.post(
                    f"{peer_url}/block/new",
                    json=block.to_dict(),
                    timeout=2
                )
                
                if response.status_code == 200:
                    print(f"✓ Block sent to {peer_id}")
                else:
                    print(f"✗ Failed to send to {peer_id}")
            except Exception as e:
                print(f"✗ Error sending to {peer_id}: {str(e)}")
    
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
        
        for peer_id, peer_url in self.peers.items():
            print(f"Checking {peer_id}...")
            chain_data = self.request_chain(peer_url)
            
            if chain_data:
                length = len(chain_data)
                
                if length > max_length:
                    max_length = length
                    longest_chain = chain_data
                    print(f"Found longer chain at {peer_id} (length: {length})")
        
        if longest_chain:
            if self.blockchain.replace_chain(longest_chain):
                print("Chain replaced with longer chain!")
                return True
        
        print("Chain is up to date")
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
