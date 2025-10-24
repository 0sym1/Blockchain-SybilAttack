"""
Example 2: P2P Network setup
Demonstrates creating nodes and connecting them
"""
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from network.node import Node
from network.network_manager import NetworkManager
from core.transaction import Transaction


def main():
    print("\n" + "="*80)
    print("EXAMPLE 2: P2P NETWORK SETUP")
    print("="*80)
    
    # 1. Create network manager
    print("\n1. Creating network manager...")
    network_manager = NetworkManager()
    print("✓ Network manager ready")
    
    # 2. Create 3 nodes
    print("\n2. Creating nodes...")
    alice = Node(username="Alice")
    bob = Node(username="Bob")
    charlie = Node(username="Charlie")
    
    print(f"✓ Alice node: {alice.get_url()}")
    print(f"✓ Bob node: {bob.get_url()}")
    print(f"✓ Charlie node: {charlie.get_url()}")
    
    # 3. Start nodes
    print("\n3. Starting nodes...")
    alice.start()
    bob.start()
    charlie.start()
    time.sleep(1)
    print("✓ All nodes started")
    
    # 4. Register to network
    print("\n4. Registering nodes to network...")
    network_manager.register_node(alice.node_id, alice.host, alice.port, alice.username)
    network_manager.register_node(bob.node_id, bob.host, bob.port, bob.username)
    network_manager.register_node(charlie.node_id, charlie.host, charlie.port, charlie.username)
    print("✓ All nodes registered")
    
    # 5. Connect nodes (create topology)
    print("\n5. Creating network topology...")
    # Alice connects to Bob and Charlie
    alice.add_peer(bob.node_id, bob.get_url())
    alice.add_peer(charlie.node_id, charlie.get_url())
    
    # Bob connects to Alice and Charlie
    bob.add_peer(alice.node_id, alice.get_url())
    bob.add_peer(charlie.node_id, charlie.get_url())
    
    # Charlie connects to Alice and Bob
    charlie.add_peer(alice.node_id, alice.get_url())
    charlie.add_peer(bob.node_id, bob.get_url())
    
    print("✓ Network topology created")
    print(f"   Alice peers: {len(alice.peers)}")
    print(f"   Bob peers: {len(bob.peers)}")
    print(f"   Charlie peers: {len(charlie.peers)}")
    
    # 6. Create and broadcast transaction
    print("\n6. Creating transaction...")
    tx = alice.create_transaction("Bob", 25)
    print(f"✓ Transaction created: {tx}")
    print(f"✓ Transaction broadcasted to {len(alice.peers)} peers")
    
    time.sleep(1)
    
    # 7. Check pending transactions
    print("\n7. Checking pending transactions...")
    print(f"   Alice: {len(alice.blockchain.pending_transactions)} pending")
    print(f"   Bob: {len(bob.blockchain.pending_transactions)} pending")
    print(f"   Charlie: {len(charlie.blockchain.pending_transactions)} pending")
    
    # 8. Bob mines the transaction
    print("\n8. Bob mining block...")
    block = bob.mine_block()
    print(f"✓ Block mined: {block.hash[:20]}...")
    
    time.sleep(1)
    
    # 9. Display network status
    print("\n9. Network status:")
    network_manager.display_network()
    
    # 10. Display each node's blockchain
    print("\n10. Blockchain status:")
    print(f"   Alice chain length: {len(alice.blockchain.chain)}")
    print(f"   Bob chain length: {len(bob.blockchain.chain)}")
    print(f"   Charlie chain length: {len(charlie.blockchain.chain)}")
    
    print("\n" + "="*80)
    print("✅ EXAMPLE 2 COMPLETED")
    print("="*80)
    print("\nNote: Nodes are still running. Press Ctrl+C to exit.")
    print("="*80 + "\n")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down...")


if __name__ == "__main__":
    main()
