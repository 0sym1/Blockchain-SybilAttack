"""
Example 3: Sybil Attack simulation
Demonstrates how Sybil attack works
"""
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from network.node import Node
from network.network_manager import NetworkManager
from attack.sybil_attack import SybilAttackSimulator
from visualization import visualize_network, visualize_attack_stats


def main():
    print("\n" + "="*80)
    print("EXAMPLE 3: SYBIL ATTACK SIMULATION")
    print("="*80)
    
    # 1. Setup honest network
    print("\n1. Setting up honest network...")
    network_manager = NetworkManager()
    
    honest_nodes = []
    for i in range(5):
        node = Node(username=f"Honest_{i+1}")
        node.start()
        time.sleep(0.1)
        
        network_manager.register_node(
            node.node_id, node.host, node.port, node.username
        )
        honest_nodes.append(node)
    
    print(f"✓ Created {len(honest_nodes)} honest nodes")
    
    # 2. Connect honest nodes
    print("\n2. Connecting honest nodes...")
    for i, node in enumerate(honest_nodes):
        # Connect to 2-3 other honest nodes
        for j in range(i+1, min(i+3, len(honest_nodes))):
            peer = honest_nodes[j]
            node.add_peer(peer.node_id, peer.get_url())
            peer.add_peer(node.node_id, node.get_url())
    
    print("✓ Honest nodes connected")
    
    # 3. Display initial network
    print("\n3. Initial network state:")
    visualize_network(network_manager)
    
    # 4. Initialize Sybil attack
    print("\n4. Initializing Sybil attack...")
    sybil_simulator = SybilAttackSimulator(network_manager)
    
    input("Press Enter to create Sybil nodes...")
    
    # 5. Create Sybil nodes
    print("\n5. Creating Sybil nodes...")
    sybil_nodes = sybil_simulator.create_sybil_nodes(count=15)
    print(f"✓ Created {len(sybil_nodes)} Sybil nodes")
    
    time.sleep(1)
    
    # 6. Connect Sybil nodes
    print("\n6. Connecting Sybil nodes...")
    sybil_simulator.connect_sybil_nodes()
    
    # 7. Display network after attack
    print("\n7. Network after attack:")
    visualize_network(network_manager)
    
    # 8. Display statistics
    print("\n8. Attack statistics:")
    total = len(honest_nodes) + len(sybil_nodes)
    visualize_attack_stats(total, len(sybil_nodes), len(honest_nodes))
    
    # 9. Analyze attack success
    print("\n9. Analyzing attack...")
    sybil_simulator.attack_network(target_percentage=0.5)
    
    # 10. Demonstrate capabilities
    print("\n10. Demonstrating attack capabilities...")
    print("\n⚠️ With control of the network, attacker can:")
    print("   • Reject valid transactions from honest nodes")
    print("   • Create alternative blockchain history")
    print("   • Eclipse individual honest nodes")
    print("   • Manipulate consensus decisions")
    print("   • Perform double-spending attacks")
    
    # 11. Cleanup option
    print("\n11. Cleanup:")
    cleanup = input("Cleanup Sybil nodes? (yes/no): ").strip().lower()
    
    if cleanup == 'yes':
        sybil_simulator.cleanup()
        print("\n✓ Network restored to honest state")
        visualize_network(network_manager)
    
    print("\n" + "="*80)
    print("✅ EXAMPLE 3 COMPLETED")
    print("="*80 + "\n")
    
    print("\n📚 Key Takeaways:")
    print("   • Sybil attack creates many fake identities")
    print("   • Can overwhelm honest nodes in the network")
    print("   • Enables various secondary attacks")
    print("   • Countermeasures: POW/POS, reputation systems")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
