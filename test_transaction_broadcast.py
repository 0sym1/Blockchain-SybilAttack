"""
Test Transaction Broadcast between 3 nodes
"""
import time
import requests
from auth.user_manager import UserManager
from network.node import Node
from network.network_manager import NetworkManager

def test_broadcast():
    """Test transaction broadcast giữa 3 nodes"""
    print("="*80)
    print("TEST: Transaction Broadcast")
    print("="*80)
    
    # Create 3 users
    um = UserManager()
    users = ['TestA', 'TestB', 'TestC']
    
    print("\n1️⃣ Creating test users...")
    for user in users:
        success, msg, data = um.register(user, 'password123')
        if success:
            print(f"   ✓ Created {user}")
        else:
            print(f"   ℹ️ {user} already exists")
    
    # Create 3 nodes
    print("\n2️⃣ Creating nodes...")
    nodes = {}
    for user in users:
        success, msg, data = um.login(user, 'password123')
        if success:
            node = Node(username=user)
            node.blockchain = node.blockchain  # Use existing blockchain
            node.start()
            nodes[user] = node
            print(f"   ✓ Started node for {user} on port {node.port}")
        else:
            print(f"   ✗ Failed to login {user}: {msg}")
            return
    
    time.sleep(2)
    
    # Check initial balances
    print("\n3️⃣ Checking initial balances...")
    for user, node in nodes.items():
        balance = node.blockchain.get_balance(user)
        print(f"   {user}: {balance} coins")
    
    # Connect nodes
    print("\n4️⃣ Connecting nodes...")
    nm = NetworkManager()
    all_nodes = nm.get_all_nodes()
    
    for user, node in nodes.items():
        for other_node in all_nodes:
            if other_node['username'] != user:
                node.add_peer(other_node['node_id'], f"http://{other_node['host']}:{other_node['port']}")
                print(f"   ✓ {user} connected to {other_node['username']}")
    
    # Check peer counts
    print("\n5️⃣ Peer counts:")
    for user, node in nodes.items():
        print(f"   {user}: {len(node.peers)} peer(s)")
    
    # IMPORTANT: Sync blockchains first!
    print("\n6️⃣ Syncing blockchains...")
    
    # Use TestA's blockchain as the master
    master_chain = nodes['TestA'].blockchain.chain
    print(f"   Master chain (TestA): {len(master_chain)} blocks")
    
    for user in ['TestB', 'TestC']:
        nodes[user].blockchain.chain = [block for block in master_chain]
        nodes[user].blockchain.pending_transactions = []
        print(f"   ✓ {user} adopted TestA's blockchain")
    
    # Verify sync
    print("\n7️⃣ Verifying blockchain sync...")
    for user, node in nodes.items():
        chain_len = len(node.blockchain.chain)
        balance = node.blockchain.get_balance('TestA')
        print(f"   {user}: {chain_len} blocks, TestA balance: {balance} coins")
    
    # Create transaction from TestA to TestB
    print("\n8️⃣ Creating transaction: TestA → TestB (50 coins)")
    try:
        tx = nodes['TestA'].create_transaction('TestB', 50)
        print(f"   ✓ Transaction created: {tx}")
        time.sleep(1)
    except Exception as e:
        print(f"   ✗ Failed: {str(e)}")
        return
    
    # Check pending transactions on all nodes
    print("\n9️⃣ Checking pending transactions...")
    for user, node in nodes.items():
        pending_count = len(node.blockchain.pending_transactions)
        print(f"   {user}: {pending_count} pending transaction(s)")
        
        if pending_count > 0:
            for tx in node.blockchain.pending_transactions:
                print(f"      → {tx.sender} → {tx.receiver}: {tx.amount} coins")
    
    # Try to mine on TestB
    print("\n🔟 TestB mining block...")
    if len(nodes['TestB'].blockchain.pending_transactions) > 0:
        block = nodes['TestB'].mine_block()
        if block:
            print(f"   ✓ Block mined! #{block.index}")
        else:
            print(f"   ✗ Mining failed")
    else:
        print(f"   ✗ No pending transactions to mine!")
    
    # Check final balances
    print("\n1️⃣1️⃣ Final balances:")
    for user, node in nodes.items():
        balance = node.blockchain.get_balance(user)
        pending = len(node.blockchain.pending_transactions)
        print(f"   {user}: {balance} coins ({pending} pending)")
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    for user, node in nodes.items():
        try:
            requests.post(f"http://{node.host}:{node.port}/shutdown", timeout=1)
        except:
            pass
        nm.unregister_node(node.node_id)
        print(f"   ✓ Stopped {user}")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    test_broadcast()
