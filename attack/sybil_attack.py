"""
Sybil Attack Simulator - Mô phỏng tấn công Sybil
"""
import time
import config
from network.node import Node
from network.network_manager import NetworkManager


class SybilAttackSimulator:
    def __init__(self, network_manager):
        """
        Khởi tạo Sybil Attack Simulator
        
        Args:
            network_manager (NetworkManager): Network manager instance
        """
        self.network_manager = network_manager
        self.sybil_nodes = []
    
    def create_sybil_nodes(self, count=None):
        """
        Tạo nhiều node giả mạo (Sybil nodes)
        
        Args:
            count (int): Số lượng Sybil nodes cần tạo
        
        Returns:
            list: Danh sách Sybil nodes
        """
        count = count or config.SYBIL_NODES_COUNT
        
        print("\n" + "="*80)
        print(f"🚨 SYBIL ATTACK SIMULATION")
        print("="*80)
        print(f"Creating {count} Sybil nodes...")
        print("="*80 + "\n")
        
        for i in range(count):
            try:
                # Tạo node giả mạo
                sybil_node = Node(username=f"Sybil_{i+1}")
                
                # Start node
                sybil_node.start()
                time.sleep(0.1)  # Đợi node khởi động
                
                # Đăng ký vào mạng
                self.network_manager.register_node(
                    node_id=sybil_node.node_id,
                    host=sybil_node.host,
                    port=sybil_node.port,
                    username=sybil_node.username
                )
                
                self.sybil_nodes.append(sybil_node)
                print(f"✓ Created Sybil node {i+1}/{count}: {sybil_node.username} (Port: {sybil_node.port})")
                
            except Exception as e:
                print(f"✗ Failed to create Sybil node {i+1}: {str(e)}")
        
        print(f"\n✅ Successfully created {len(self.sybil_nodes)} Sybil nodes!")
        print(f"📊 Network size: {self.network_manager.get_network_size()} nodes")
        print("="*80 + "\n")
        
        return self.sybil_nodes
    
    def connect_sybil_nodes(self):
        """
        Kết nối các Sybil nodes với nhau để tạo thành một nhóm
        """
        print("\n" + "="*80)
        print("🔗 Connecting Sybil nodes to each other...")
        print("="*80 + "\n")
        
        # Kết nối mỗi Sybil node với một số Sybil nodes khác
        for i, sybil_node in enumerate(self.sybil_nodes):
            # Kết nối với 3-5 Sybil nodes khác
            start_idx = (i + 1) % len(self.sybil_nodes)
            end_idx = (i + 5) % len(self.sybil_nodes)
            
            if start_idx < end_idx:
                peers_to_connect = self.sybil_nodes[start_idx:end_idx]
            else:
                peers_to_connect = self.sybil_nodes[start_idx:] + self.sybil_nodes[:end_idx]
            
            for peer in peers_to_connect:
                if peer.node_id != sybil_node.node_id:
                    sybil_node.add_peer(peer.node_id, peer.get_url())
            
            print(f"✓ {sybil_node.username} connected to {len(sybil_node.peers)} peers")
        
        print("\n✅ Sybil nodes are now interconnected!")
        print("="*80 + "\n")
    
    def attack_network(self, target_percentage=0.5):
        """
        Thực hiện Sybil attack bằng cách chiếm phần lớn mạng
        
        Args:
            target_percentage (float): Tỷ lệ mạng muốn chiếm (0.0 - 1.0)
        """
        network_size = self.network_manager.get_network_size()
        honest_nodes = network_size - len(self.sybil_nodes)
        
        print("\n" + "="*80)
        print("⚔️ EXECUTING SYBIL ATTACK")
        print("="*80)
        print(f"Network statistics:")
        print(f"  - Total nodes: {network_size}")
        print(f"  - Honest nodes: {honest_nodes}")
        print(f"  - Sybil nodes: {len(self.sybil_nodes)}")
        print(f"  - Sybil ratio: {len(self.sybil_nodes)/network_size*100:.1f}%")
        print("="*80)
        
        if len(self.sybil_nodes) / network_size >= target_percentage:
            print(f"\n✅ ATTACK SUCCESSFUL!")
            print(f"Sybil nodes control {len(self.sybil_nodes)/network_size*100:.1f}% of the network!")
            print("\nAttack capabilities:")
            print("  - Can influence consensus")
            print("  - Can reject valid transactions")
            print("  - Can perform Eclipse attacks on honest nodes")
            print("  - Can control network routing")
        else:
            print(f"\n⚠️ ATTACK IN PROGRESS")
            print(f"Need more Sybil nodes to reach {target_percentage*100:.0f}% control")
        
        print("="*80 + "\n")
    
    def cleanup(self):
        """Dọn dẹp các Sybil nodes"""
        print("\n" + "="*80)
        print("🧹 Cleaning up Sybil nodes...")
        print("="*80 + "\n")
        
        for sybil_node in self.sybil_nodes:
            try:
                # Xóa khỏi network
                self.network_manager.unregister_node(sybil_node.node_id)
                print(f"✓ Removed {sybil_node.username}")
            except Exception as e:
                print(f"✗ Error removing {sybil_node.username}: {str(e)}")
        
        self.sybil_nodes.clear()
        print("\n✅ Cleanup complete!")
        print("="*80 + "\n")
    
    def demonstrate_attack(self):
        """
        Demo đầy đủ Sybil attack
        """
        print("\n" + "="*80)
        print("🎯 SYBIL ATTACK DEMONSTRATION")
        print("="*80)
        print("\nSybil Attack: Tấn công bằng cách tạo nhiều node giả mạo")
        print("để chiếm đoạt quyền kiểm soát mạng blockchain.")
        print("\nPhases:")
        print("  1. Create multiple fake identities (Sybil nodes)")
        print("  2. Join the network")
        print("  3. Gain majority control")
        print("  4. Manipulate network behavior")
        print("="*80 + "\n")
        
        input("Press Enter to start Phase 1: Creating Sybil nodes...")
        self.create_sybil_nodes()
        
        input("Press Enter to start Phase 2: Connecting Sybil nodes...")
        self.connect_sybil_nodes()
        
        input("Press Enter to start Phase 3: Analyzing attack success...")
        self.attack_network()
        
        print("\n💡 Impact of Sybil Attack:")
        print("  - Network decentralization is compromised")
        print("  - Honest nodes can be isolated (Eclipse Attack)")
        print("  - Consensus can be manipulated")
        print("  - Double-spending becomes possible")
        print("\n🛡️ Countermeasures:")
        print("  - Proof of Work/Stake requirements")
        print("  - Identity verification")
        print("  - Reputation systems")
        print("  - IP address restrictions")
        print("="*80 + "\n")
