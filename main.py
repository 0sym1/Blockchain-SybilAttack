"""
Main Entry Point - Blockchain Sybil & Eclipse Attack Demo
"""
import time
import os
import sys
import socket
import subprocess

from auth.user_manager import UserManager
from network.node import Node
from network.network_manager import NetworkManager
from network.peer_discovery import PeerDiscovery
from attack.sybil_attack import SybilAttackSimulator
from attack.eclipse_attack import EclipseAttackSimulator
from core.blockchain import Blockchain
import config


def kill_process_on_port(port):
    """
    Kill process đang chạy trên port (Windows & Linux compatible)
    
    Args:
        port (int): Port number
    """
    try:
        if os.name == 'nt':  # Windows
            # Tìm PID của process trên port
            result = subprocess.run(
                ['netstat', '-ano'], 
                capture_output=True, 
                text=True,
                timeout=5
            )
            for line in result.stdout.split('\n'):
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    pid = parts[-1]
                    # Kill process
                    subprocess.run(['taskkill', '/F', '/PID', pid], 
                                   capture_output=True, timeout=5)
                    print(f"🔪 Killed process {pid} on port {port}")
                    break
        else:  # Linux/Mac
            result = subprocess.run(
                ['lsof', '-ti', f':{port}'], 
                capture_output=True, 
                text=True,
                timeout=5
            )
            if result.stdout:
                pid = result.stdout.strip()
                subprocess.run(['kill', '-9', pid], timeout=5)
                print(f"🔪 Killed process {pid} on port {port}")
    except Exception as e:
        pass  # Bỏ qua lỗi, port có thể đã free


class BlockchainSystem:
    def __init__(self):
        """Khởi tạo hệ thống blockchain"""
        self.user_manager = UserManager()
        self.network_manager = NetworkManager()
        self.current_user = None
        self.current_node = None
        self.peer_discovery = None
        
        print("\n" + "="*80)
        print("🔗 BLOCKCHAIN SYSTEM - SYBIL & ECLIPSE ATTACK DEMO")
        print("="*80)
        print("Welcome to the Blockchain Attack Demonstration System!")
        print("="*80 + "\n")
    
    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Hiển thị menu chính"""
        print("\n" + "="*80)
        print("MAIN MENU")
        print("="*80)
        
        if self.current_user:
            print(f"👤 Logged in as: {self.current_user}")
            if self.current_node:
                print(f"🌐 Node: {self.current_node.get_url()}")
                print(f"💰 Balance: {self.current_node.get_balance()} coins")
                print(f"👥 Peers: {len(self.current_node.peers)}/{config.MAX_PEERS}")
        
        print("\n📋 Account Management:")
        print("  1. Register new account")
        print("  2. Login")
        print("  3. Logout")
        print("  4. List all accounts")
        
        if self.current_node:
            print("\n💼 Blockchain Operations:")
            print("  5. View blockchain")
            print("  6. Create transaction")
            print("  7. Mine block")
            print("  8. Check balance")
            print("  9. Validate blockchain")
            
            print("\n🌐 Network Operations:")
            print("  10. View node info")
            print("  11. Connect to peers")
            print("  12. View network status")
            print("  13. Synchronize blockchain")
            print("  14. Cleanup dead peers")
        
        print("\n⚔️ Attack Simulations:")
        print("  15. Demonstrate Sybil Attack")
        print("  16. Demonstrate Eclipse Attack")
        
        print("\n  0. Exit")
        print("="*80)
    
    def register_account(self):
        """Đăng ký tài khoản mới"""
        print("\n" + "="*80)
        print("REGISTER NEW ACCOUNT")
        print("="*80)
        
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        success, message, blockchain_data = self.user_manager.register(username, password)
        
        print(f"\n{message}")
        
        if success:
            print(f"✅ Account '{username}' created successfully!")
            print(f"📦 Genesis block initialized")
    
    def login(self):
        """Đăng nhập"""
        print("\n" + "="*80)
        print("LOGIN")
        print("="*80)
        
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        success, message, account_data = self.user_manager.login(username, password)
        
        if success:
            self.current_user = username
            
            # Cleanup old nodes của username này nếu có
            print(f"\n🧹 Checking for old nodes...")
            old_nodes = [
                node for node in self.network_manager.get_all_nodes() 
                if node['username'] == username
            ]
            
            if old_nodes:
                print(f"⚠️ Found {len(old_nodes)} old node(s) for {username}, cleaning up...")
                for old_node in old_nodes:
                    # Kill process trên port cũ
                    old_port = old_node.get('port')
                    if old_port:
                        kill_process_on_port(old_port)
                    
                    # Unregister node
                    self.network_manager.unregister_node(old_node['node_id'])
                    print(f"   ✓ Removed old node {old_node['node_id'][:8]}... (port {old_port})")
            
            # Tạo node cho user
            print(f"\n🚀 Creating node for {username}...")
            self.current_node = Node(username=username)
            
            # Load blockchain từ account
            if account_data.get('blockchain'):
                try:
                    self.current_node.blockchain = Blockchain.from_list(
                        account_data['blockchain'],
                        owner_address=username
                    )
                    print(f"✅ Blockchain loaded (Length: {len(self.current_node.blockchain.chain)})")
                    
                    # Hiển thị balance (chỉ confirmed)
                    balance = self.current_node.blockchain.get_balance(username)
                    print(f"💰 Confirmed balance: {balance} coins")
                except Exception as e:
                    print(f"⚠️ Failed to load blockchain: {str(e)}, using new one")
            
            # Start node
            self.current_node.start()
            time.sleep(1)  # Đợi node khởi động
            
            # Đăng ký vào network
            self.network_manager.register_node(
                node_id=self.current_node.node_id,
                host=self.current_node.host,
                port=self.current_node.port,
                username=username
            )
            
            # Update account với node_id
            self.user_manager.update_account(username, node_id=self.current_node.node_id)
            
            # Khởi tạo peer discovery
            self.peer_discovery = PeerDiscovery(self.current_node)
            
            # Tự động kết nối với peers
            print(f"\n🔍 Discovering peers...")
            connected_peers = self.peer_discovery.discover_peers(self.network_manager)
            print(f"✅ Connected to {len(connected_peers)} peers")
            
            print(f"\n✅ Login successful! Welcome {username}!")
            print(f"🌐 Node URL: {self.current_node.get_url()}")
        else:
            print(f"\n❌ {message}")
    
    def logout(self):
        """Đăng nhập"""
        if not self.current_user:
            print("\n❌ Not logged in!")
            return
        
        print(f"\n👋 Logging out {self.current_user}...")
        
        # Lưu blockchain vào account
        if self.current_node:
            blockchain_data = self.current_node.blockchain.to_list()
            self.user_manager.update_account(self.current_user, blockchain_data=blockchain_data)
            
            # Unregister từ network
            self.network_manager.unregister_node(self.current_node.node_id)
            
            # Stop Flask server
            print("🛑 Stopping node server...")
            self.current_node.stop()
        
        self.current_user = None
        self.current_node = None
        self.peer_discovery = None
        
        print("✅ Logged out successfully!")
    
    def list_accounts(self):
        """Liệt kê tài khoản"""
        self.user_manager.display_accounts()
    
    def view_blockchain(self):
        """Xem blockchain"""
        if not self.current_node:
            print("\n❌ Please login first!")
            return
        
        self.current_node.blockchain.display_chain()
    
    def create_transaction(self):
        """Tạo giao dịch"""
        if not self.current_node:
            print("\n❌ Please login first!")
            return
        
        print("\n" + "="*80)
        print("CREATE TRANSACTION")
        print("="*80)
        
        # Hiển thị balance hiện tại
        confirmed, pending, total = self.current_node.blockchain.get_total_balance(
            self.current_node.username
        )
        print(f"💰 Your confirmed balance: {confirmed} coins")
        if pending != 0:
            print(f"⏳ Pending: {pending} coins (Total: {total} coins)")
        
        receiver = input("\nReceiver address: ").strip()
        
        try:
            amount = float(input("Amount: ").strip())
        except ValueError:
            print("❌ Invalid amount!")
            return
        
        # Validate amount
        if amount <= 0:
            print("❌ Amount must be greater than 0!")
            return
        
        # Tạo transaction (validation ở trong node.create_transaction)
        try:
            transaction = self.current_node.create_transaction(receiver, amount)
            print(f"\n✅ Transaction created and broadcasted!")
            print(f"📤 {transaction}")
            print(f"\n💡 Transaction is pending. Mine a block to confirm it!")
        except ValueError as e:
            print(f"\n❌ Transaction failed: {str(e)}")
    
    def mine_block(self):
        """Mine block"""
        if not self.current_node:
            print("\n❌ Please login first!")
            return
        
        print("\n" + "="*80)
        print("MINING BLOCK")
        print("="*80)
        
        if not self.current_node.blockchain.pending_transactions:
            print("❌ No pending transactions to mine!")
            return
        
        print(f"⛏️ Mining with difficulty {self.current_node.blockchain.difficulty}...")
        print("This may take a moment...\n")
        
        block = self.current_node.mine_block()
        
        if block:
            print(f"\n✅ Block #{block.index} mined successfully!")
            print(f"💎 Hash: {block.hash}")
            print(f"🎁 Mining reward: {config.MINING_REWARD} coins")
    
    def check_balance(self):
        """Kiểm tra số dư"""
        if not self.current_node:
            print("\n❌ Please login first!")
            return
        
        # Get detailed balance info
        confirmed, pending, total = self.current_node.blockchain.get_total_balance(
            self.current_node.username
        )
        
        print("\n" + "="*60)
        print("💰 BALANCE INFORMATION")
        print("="*60)
        print(f"✅ Confirmed Balance: {confirmed} coins")
        print(f"⏳ Pending Balance:   {pending} coins")
        print(f"📊 Total Balance:     {total} coins")
        print("="*60)
        
        if pending != 0:
            print("\n💡 Tip: Pending transactions need to be mined to be confirmed")
            print(f"   You have {len(self.current_node.blockchain.pending_transactions)} pending transaction(s)")
    
    def validate_blockchain(self):
        """Validate blockchain"""
        if not self.current_node:
            print("\n❌ Please login first!")
            return
        
        print("\n🔍 Validating blockchain...")
        is_valid = self.current_node.blockchain.is_chain_valid()
        
        if is_valid:
            print("✅ Blockchain is valid!")
        else:
            print("❌ Blockchain is invalid!")
    
    def view_node_info(self):
        """Xem thông tin node"""
        if not self.current_node:
            print("\n❌ Please login first!")
            return
        
        self.current_node.display_info()
    
    def connect_to_peers(self):
        """Kết nối với peers"""
        if not self.current_node:
            print("\n❌ Please login first!")
            return
        
        print("\n🔍 Discovering and connecting to peers...")
        connected_peers = self.peer_discovery.discover_peers(self.network_manager)
        
        print(f"\n✅ Connected to {len(connected_peers)} new peers")
        print(f"📊 Total peers: {len(self.current_node.peers)}/{config.MAX_PEERS}")
    
    def view_network_status(self):
        """Xem trạng thái mạng"""
        self.network_manager.display_network()
    
    def synchronize_blockchain(self):
        """Đồng bộ blockchain"""
        if not self.current_node:
            print("\n❌ Please login first!")
            return
        
        print("\n🔄 Synchronizing blockchain with peers...")
        replaced = self.current_node.resolve_conflicts()
        
        if replaced:
            print("✅ Blockchain updated with longer chain from peers!")
        else:
            print("✅ Your blockchain is up to date!")
    
    def cleanup_dead_peers(self):
        """Xóa các peers đã chết"""
        if not self.current_node:
            print("\n❌ Please login first!")
            return
        
        print("\n🧹 Cleaning up dead peers...")
        print(f"Current peers: {len(self.current_node.peers)}/{config.MAX_PEERS}")
        
        removed = self.current_node.cleanup_stale_peers()
        
        if removed > 0:
            print(f"\n✅ Removed {removed} dead peer(s)")
            print(f"💡 You now have {len(self.current_node.peers)}/{config.MAX_PEERS} active peers")
            print(f"   {config.MAX_PEERS - len(self.current_node.peers)} slot(s) available for new connections")
        else:
            print("\n✅ All peers are healthy!")
    
    def demonstrate_sybil_attack(self):
        """Demo Sybil attack"""
        print("\n⚠️ WARNING: This will create many nodes and may consume resources!")
        confirm = input("Continue? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("❌ Attack demonstration cancelled")
            return
        
        # Khởi tạo Sybil attack simulator
        sybil_simulator = SybilAttackSimulator(self.network_manager)
        
        # Demo attack
        sybil_simulator.demonstrate_attack()
        
        # Cleanup option
        cleanup = input("\nCleanup Sybil nodes? (yes/no): ").strip().lower()
        if cleanup == 'yes':
            sybil_simulator.cleanup()
    
    def demonstrate_eclipse_attack(self):
        """Demo Eclipse attack"""
        if not self.current_node:
            print("\n❌ Please login first! You need a target node.")
            return
        
        print("\n⚠️ WARNING: This will isolate your current node!")
        confirm = input("Continue? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("❌ Attack demonstration cancelled")
            return
        
        # Khởi tạo Eclipse attack simulator
        eclipse_simulator = EclipseAttackSimulator(self.network_manager)
        
        # Demo attack on current node
        eclipse_simulator.demonstrate_attack(self.current_node)
        
        # Cleanup option
        cleanup = input("\nCleanup and restore connections? (yes/no): ").strip().lower()
        if cleanup == 'yes':
            eclipse_simulator.cleanup()
            # Reconnect to normal peers
            if self.peer_discovery:
                self.peer_discovery.discover_peers(self.network_manager)
    
    def run(self):
        """Chạy hệ thống"""
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice: ").strip()
                
                if choice == '0':
                    print("\n👋 Thank you for using the Blockchain System!")
                    if self.current_node:
                        self.logout()
                    break
                elif choice == '1':
                    self.register_account()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    self.logout()
                elif choice == '4':
                    self.list_accounts()
                elif choice == '5':
                    self.view_blockchain()
                elif choice == '6':
                    self.create_transaction()
                elif choice == '7':
                    self.mine_block()
                elif choice == '8':
                    self.check_balance()
                elif choice == '9':
                    self.validate_blockchain()
                elif choice == '10':
                    self.view_node_info()
                elif choice == '11':
                    self.connect_to_peers()
                elif choice == '12':
                    self.view_network_status()
                elif choice == '13':
                    self.synchronize_blockchain()
                elif choice == '14':
                    self.cleanup_dead_peers()
                elif choice == '15':
                    self.demonstrate_sybil_attack()
                elif choice == '16':
                    self.demonstrate_eclipse_attack()
                else:
                    print("\n❌ Invalid choice! Please try again.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Exiting...")
                if self.current_node:
                    self.logout()
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                import traceback
                traceback.print_exc()
                input("\nPress Enter to continue...")


def main():
    """Main function"""
    # Khởi tạo và chạy hệ thống
    system = BlockchainSystem()
    system.run()


if __name__ == "__main__":
    main()
