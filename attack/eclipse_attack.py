"""
Eclipse Attack Simulator - Mô phỏng tấn công Eclipse
"""
import time
import config
from network.node import Node
from network.network_manager import NetworkManager


class EclipseAttackSimulator:
    def __init__(self, network_manager):
        """
        Khởi tạo Eclipse Attack Simulator
        
        Args:
            network_manager (NetworkManager): Network manager instance
        """
        self.network_manager = network_manager
        self.malicious_nodes = []
        self.target_node = None
    
    def create_malicious_nodes(self, count=None):
        """
        Tạo các node độc hại
        
        Args:
            count (int): Số lượng malicious nodes
        
        Returns:
            list: Danh sách malicious nodes
        """
        count = count or config.ECLIPSE_MALICIOUS_NODES
        
        print("\n" + "="*80)
        print(f"🌑 ECLIPSE ATTACK SIMULATION")
        print("="*80)
        print(f"Creating {count} malicious nodes...")
        print("="*80 + "\n")
        
        for i in range(count):
            try:
                # Tạo malicious node
                mal_node = Node(username=f"Malicious_{i+1}")
                
                # Start node
                mal_node.start()
                time.sleep(0.1)
                
                # Đăng ký vào mạng
                self.network_manager.register_node(
                    node_id=mal_node.node_id,
                    host=mal_node.host,
                    port=mal_node.port,
                    username=mal_node.username
                )
                
                self.malicious_nodes.append(mal_node)
                print(f"✓ Created malicious node {i+1}/{count}: {mal_node.username} (Port: {mal_node.port})")
                
            except Exception as e:
                print(f"✗ Failed to create malicious node {i+1}: {str(e)}")
        
        print(f"\n✅ Successfully created {len(self.malicious_nodes)} malicious nodes!")
        print("="*80 + "\n")
        
        return self.malicious_nodes
    
    def eclipse_node(self, target_node):
        """
        Thực hiện Eclipse attack trên target node
        
        Args:
            target_node (Node): Node mục tiêu
        
        Returns:
            bool: True nếu attack thành công
        """
        self.target_node = target_node
        
        print("\n" + "="*80)
        print(f"⚔️ EXECUTING ECLIPSE ATTACK ON: {target_node.username}")
        print("="*80)
        print(f"Target node: {target_node.username} ({target_node.get_url()})")
        print(f"Current peers: {len(target_node.peers)}")
        print("="*80 + "\n")
        
        # Phase 1: Disconnect target từ honest peers
        print("Phase 1: Isolating target node from honest peers...")
        original_peers = list(target_node.peers.keys())
        
        for peer_id in original_peers:
            target_node.remove_peer(peer_id)
            print(f"  ✓ Disconnected from {peer_id[:8]}...")
        
        print(f"  ✅ Target isolated! ({len(target_node.peers)} peers remaining)\n")
        
        # Phase 2: Connect tất cả malicious nodes với target
        print("Phase 2: Surrounding target with malicious nodes...")
        
        for mal_node in self.malicious_nodes:
            # Target connects to malicious node
            target_node.add_peer(mal_node.node_id, mal_node.get_url())
            
            # Malicious node connects back
            mal_node.add_peer(target_node.node_id, target_node.get_url())
            
            print(f"  ✓ Connected to {mal_node.username}")
        
        print(f"\n  ✅ Eclipse complete! Target has {len(target_node.peers)} malicious peers\n")
        
        # Phase 3: Verify attack
        print("Phase 3: Verifying Eclipse attack...")
        
        all_malicious = all(
            peer_id in [node.node_id for node in self.malicious_nodes]
            for peer_id in target_node.peers.keys()
        )
        
        if all_malicious and len(target_node.peers) == len(self.malicious_nodes):
            print("  ✅ ATTACK SUCCESSFUL!")
            print(f"  🎯 Target node is completely eclipsed!")
            print(f"  📊 All {len(target_node.peers)} connections controlled by attacker")
            
            print("\n" + "="*80)
            print("Attack capabilities:")
            print("  - Control all information received by target")
            print("  - Feed false blockchain data")
            print("  - Reject target's transactions")
            print("  - Perform double-spending attacks")
            print("  - Prevent target from receiving valid blocks")
            print("="*80 + "\n")
            
            return True
        else:
            print("  ⚠️ ATTACK PARTIALLY SUCCESSFUL")
            print(f"  Target still has some honest connections")
            return False
    
    def demonstrate_false_chain(self):
        """
        Demo việc feed false blockchain cho eclipsed node
        """
        if not self.target_node:
            print("No target node is currently eclipsed!")
            return
        
        print("\n" + "="*80)
        print("🎭 DEMONSTRATING FALSE CHAIN ATTACK")
        print("="*80)
        
        # Tạo fake transaction
        print("\nCreating fake transaction from malicious node...")
        fake_tx = self.malicious_nodes[0].create_transaction(
            receiver=self.malicious_nodes[0].username,
            amount=1000000  # Unrealistic amount
        )
        
        print(f"✓ Fake transaction created: {fake_tx}")
        
        # Mine fake block
        print("\nMining fake block...")
        fake_block = self.malicious_nodes[0].mine_block()
        
        if fake_block:
            print(f"✓ Fake block mined: Block #{fake_block.index}")
            
            # Broadcast chỉ đến target (eclipsed node)
            print(f"\nBroadcasting fake block to eclipsed target...")
            print(f"✓ Target ({self.target_node.username}) receives fake data")
            print(f"✓ Honest network remains unaware")
            
            print("\n" + "="*80)
            print("Impact:")
            print(f"  - Target believes fake chain is valid")
            print(f"  - Target's view of network state is manipulated")
            print(f"  - Target can be tricked into accepting invalid transactions")
            print("="*80 + "\n")
    
    def cleanup(self):
        """Dọn dẹp malicious nodes và restore target"""
        print("\n" + "="*80)
        print("🧹 Cleaning up Eclipse attack...")
        print("="*80 + "\n")
        
        # Disconnect target from malicious nodes
        if self.target_node:
            print(f"Restoring {self.target_node.username}...")
            for mal_node in self.malicious_nodes:
                self.target_node.remove_peer(mal_node.node_id)
            print(f"✓ Target node restored\n")
        
        # Remove malicious nodes
        for mal_node in self.malicious_nodes:
            try:
                self.network_manager.unregister_node(mal_node.node_id)
                print(f"✓ Removed {mal_node.username}")
            except Exception as e:
                print(f"✗ Error removing {mal_node.username}: {str(e)}")
        
        self.malicious_nodes.clear()
        self.target_node = None
        
        print("\n✅ Cleanup complete!")
        print("="*80 + "\n")
    
    def demonstrate_attack(self, target_node):
        """
        Demo đầy đủ Eclipse attack
        
        Args:
            target_node (Node): Node mục tiêu
        """
        print("\n" + "="*80)
        print("🎯 ECLIPSE ATTACK DEMONSTRATION")
        print("="*80)
        print("\nEclipse Attack: Tấn công bằng cách kiểm soát tất cả")
        print("kết nối của một node, cô lập nó khỏi mạng thật.")
        print("\nPhases:")
        print("  1. Create malicious nodes")
        print("  2. Isolate target from honest peers")
        print("  3. Surround target with malicious nodes")
        print("  4. Feed false information to target")
        print("="*80 + "\n")
        
        input("Press Enter to start Phase 1: Creating malicious nodes...")
        self.create_malicious_nodes()
        
        input(f"Press Enter to start Phase 2-3: Eclipsing {target_node.username}...")
        self.eclipse_node(target_node)
        
        input("Press Enter to start Phase 4: Demonstrating false chain attack...")
        self.demonstrate_false_chain()
        
        print("\n💡 Impact of Eclipse Attack:")
        print("  - Target is isolated from honest network")
        print("  - Target receives only attacker-controlled information")
        print("  - Can enable double-spending attacks")
        print("  - Target's transactions can be blocked")
        print("\n🛡️ Countermeasures:")
        print("  - Diverse peer selection")
        print("  - Regular peer rotation")
        print("  - Multiple network paths")
        print("  - Peer reputation systems")
        print("="*80 + "\n")
