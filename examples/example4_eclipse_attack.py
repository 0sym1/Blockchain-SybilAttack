"""
Example 4: Eclipse Attack simulation
Demonstrates how Eclipse attack isolates a node
"""
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from network.node import Node
from network.network_manager import NetworkManager
from attack.eclipse_attack import EclipseAttackSimulator
from visualization import visualize_network, visualize_eclipse
from core.transaction import Transaction


def main():
    print("\n" + "="*80)
    print("EXAMPLE 4: ECLIPSE ATTACK SIMULATION")
    print("="*80)
    
    # 1. Setup network
    print("\n1. Setting up network...")
    network_manager = NetworkManager()
    
    # Create honest nodes
    honest_nodes = []
    for i in range(10):
        node = Node(username=f"Honest_{i+1}")
        node.start()
        time.sleep(0.1)
        
        network_manager.register_node(
            node.node_id, node.host, node.port, node.username
        )
        honest_nodes.append(node)
    
    print(f"✓ Created {len(honest_nodes)} honest nodes")
    
    # 2. Create target node (victim)
    print("\n2. Creating target node (victim)...")
    target = Node(username="Target_Alice")
    target.start()
    time.sleep(0.5)
    
    network_manager.register_node(
        target.node_id, target.host, target.port, target.username
    )
    
    print(f"✓ Target node: {target.username} ({target.get_url()})")
    
    # 3. Connect target to honest nodes
    print("\n3. Connecting target to honest nodes...")
    for i in range(5):  # Connect to 5 honest nodes
        peer = honest_nodes[i]
        target.add_peer(peer.node_id, peer.get_url())
        peer.add_peer(target.node_id, target.get_url())
    
    print(f"✓ Target connected to {len(target.peers)} honest peers")
    
    # 4. Create some transactions
    print("\n4. Creating transactions in honest network...")
    tx1 = honest_nodes[0].create_transaction("Target_Alice", 100)
    time.sleep(0.5)
    
    # Target mines a block
    print("\n5. Target mining block...")
    block = target.mine_block()
    print(f"✓ Block mined: {block.hash[:20]}...")
    
    # 6. Display initial state
    print("\n6. Initial network state:")
    print(f"   Target peers: {len(target.peers)}")
    print(f"   Target balance: {target.get_balance()} coins")
    print(f"   Target chain length: {len(target.blockchain.chain)}")
    
    visualize_network(network_manager, highlight_nodes=[target.node_id])
    
    input("\nPress Enter to start Eclipse attack...")
    
    # 7. Initialize Eclipse attack
    print("\n7. Initializing Eclipse attack...")
    eclipse_simulator = EclipseAttackSimulator(network_manager)
    
    # 8. Create malicious nodes
    print("\n8. Creating malicious nodes...")
    malicious_nodes = eclipse_simulator.create_malicious_nodes(count=8)
    print(f"✓ Created {len(malicious_nodes)} malicious nodes")
    
    time.sleep(1)
    
    input("Press Enter to eclipse the target...")
    
    # 9. Execute Eclipse attack
    print("\n9. Executing Eclipse attack...")
    success = eclipse_simulator.eclipse_node(target)
    
    # 10. Display attack result
    print("\n10. Attack result:")
    print(f"   Target peers: {len(target.peers)}")
    print(f"   All malicious? {all(p in [n.node_id for n in malicious_nodes] for p in target.peers)}")
    
    visualize_eclipse(target, malicious_nodes)
    
    # 11. Demonstrate false information
    print("\n11. Demonstrating false blockchain...")
    
    input("Press Enter to feed fake transactions to target...")
    
    # Malicious nodes create fake transactions
    fake_tx = malicious_nodes[0].create_transaction("Malicious_1", 1000000)
    print(f"✓ Fake transaction: {fake_tx}")
    
    # Mine fake block
    fake_block = malicious_nodes[0].mine_block()
    print(f"✓ Fake block mined: {fake_block.hash[:20]}...")
    
    print("\n⚠️ Target is now isolated and receiving false information!")
    print("   • Target believes fake chain is real")
    print("   • Honest network doesn't see fake transactions")
    print("   • Target can be tricked into invalid transactions")
    print("   • Double-spending becomes possible")
    
    # 12. Show isolation
    print("\n12. Network isolation visualization:")
    visualize_network(network_manager, highlight_nodes=[target.node_id] + [n.node_id for n in malicious_nodes])
    
    # 13. Cleanup option
    print("\n13. Cleanup:")
    cleanup = input("Restore target connections? (yes/no): ").strip().lower()
    
    if cleanup == 'yes':
        eclipse_simulator.cleanup()
        
        # Reconnect to honest nodes
        print("\n   Reconnecting to honest nodes...")
        for i in range(3):
            peer = honest_nodes[i]
            if peer.node_id not in target.peers:
                target.add_peer(peer.node_id, peer.get_url())
        
        print(f"✓ Target restored: {len(target.peers)} honest peers")
        
        # Sync blockchain
        print("\n   Synchronizing blockchain...")
        target.resolve_conflicts()
        print(f"✓ Chain synchronized: {len(target.blockchain.chain)} blocks")
    
    print("\n" + "="*80)
    print("✅ EXAMPLE 4 COMPLETED")
    print("="*80 + "\n")
    
    print("\n📚 Key Takeaways:")
    print("   • Eclipse attack isolates a specific node")
    print("   • Attacker controls all connections to victim")
    print("   • Victim receives only attacker-controlled information")
    print("   • Enables sophisticated attacks like double-spending")
    print("   • Countermeasures: diverse peers, peer rotation, monitoring")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
