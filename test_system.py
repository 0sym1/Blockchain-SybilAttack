"""
Quick test script để verify hệ thống hoạt động
"""
import sys
import time
from core.blockchain import Blockchain
from core.transaction import Transaction
from network.node import Node
from network.network_manager import NetworkManager
from auth.user_manager import UserManager


def test_blockchain_basic():
    """Test blockchain cơ bản"""
    print("\n" + "="*80)
    print("TEST 1: BLOCKCHAIN BASIC OPERATIONS")
    print("="*80)
    
    # Tạo blockchain
    blockchain = Blockchain()
    print(f"✓ Genesis block created")
    
    # Tạo transaction
    tx1 = Transaction("Alice", "Bob", 50)
    blockchain.add_transaction(tx1)
    print(f"✓ Transaction added: {tx1}")
    
    # Mine block
    block = blockchain.mine_pending_transactions("Alice")
    print(f"✓ Block mined: {block}")
    
    # Validate
    is_valid = blockchain.is_chain_valid()
    print(f"✓ Chain valid: {is_valid}")
    
    assert is_valid, "Blockchain should be valid"
    assert len(blockchain.chain) == 2, "Should have 2 blocks"
    
    print("✅ TEST 1 PASSED\n")


def test_user_management():
    """Test đăng ký/đăng nhập"""
    print("\n" + "="*80)
    print("TEST 2: USER MANAGEMENT")
    print("="*80)
    
    user_manager = UserManager()
    
    # Đăng ký
    success, msg, data = user_manager.register("test_user", "password123")
    print(f"✓ Register: {msg}")
    assert success, "Registration should succeed"
    
    # Đăng nhập thành công
    success, msg, data = user_manager.login("test_user", "password123")
    print(f"✓ Login success: {msg}")
    assert success, "Login should succeed"
    
    # Đăng nhập sai password
    success, msg, data = user_manager.login("test_user", "wrong_password")
    print(f"✓ Login fail: {msg}")
    assert not success, "Login should fail with wrong password"
    
    # Cleanup
    user_manager.delete_account("test_user")
    print(f"✓ Cleanup done")
    
    print("✅ TEST 2 PASSED\n")


def test_network():
    """Test networking"""
    print("\n" + "="*80)
    print("TEST 3: NETWORK OPERATIONS")
    print("="*80)
    
    network_manager = NetworkManager()
    
    # Tạo 2 nodes
    node1 = Node(username="TestNode1")
    node2 = Node(username="TestNode2")
    
    print(f"✓ Node 1 created on port {node1.port}")
    print(f"✓ Node 2 created on port {node2.port}")
    
    # Start nodes
    node1.start()
    node2.start()
    time.sleep(1)
    
    # Register nodes
    network_manager.register_node(
        node1.node_id, node1.host, node1.port, node1.username
    )
    network_manager.register_node(
        node2.node_id, node2.host, node2.port, node2.username
    )
    
    print(f"✓ Nodes registered to network")
    
    # Kết nối
    node1.add_peer(node2.node_id, node2.get_url())
    node2.add_peer(node1.node_id, node1.get_url())
    
    print(f"✓ Nodes connected")
    
    assert len(node1.peers) == 1, "Node1 should have 1 peer"
    assert len(node2.peers) == 1, "Node2 should have 1 peer"
    
    # Cleanup
    network_manager.unregister_node(node1.node_id)
    network_manager.unregister_node(node2.node_id)
    
    print("✅ TEST 3 PASSED\n")


def test_transaction_broadcast():
    """Test broadcast transaction"""
    print("\n" + "="*80)
    print("TEST 4: TRANSACTION BROADCAST")
    print("="*80)
    
    # Tạo 2 nodes
    node1 = Node(username="Sender")
    node2 = Node(username="Receiver")
    
    node1.start()
    node2.start()
    time.sleep(1)
    
    # Kết nối
    node1.add_peer(node2.node_id, node2.get_url())
    node2.add_peer(node1.node_id, node1.get_url())
    
    print(f"✓ Nodes connected")
    
    # Node1 tạo transaction
    print(f"✓ Creating transaction...")
    tx = node1.create_transaction("Receiver", 100)
    
    time.sleep(1)  # Đợi broadcast
    
    # Kiểm tra node1 có transaction
    assert len(node1.blockchain.pending_transactions) > 0
    print(f"✓ Node1 has {len(node1.blockchain.pending_transactions)} pending tx")
    
    print("✅ TEST 4 PASSED\n")


def test_mining():
    """Test mining"""
    print("\n" + "="*80)
    print("TEST 5: MINING")
    print("="*80)
    
    node = Node(username="Miner")
    
    # Thêm transaction
    tx = Transaction("Alice", "Bob", 50)
    node.blockchain.add_transaction(tx)
    
    print(f"✓ Transaction added")
    
    # Mine
    initial_length = len(node.blockchain.chain)
    print(f"✓ Initial chain length: {initial_length}")
    
    print(f"✓ Mining block...")
    block = node.mine_block()
    
    assert block is not None, "Block should be mined"
    assert len(node.blockchain.chain) == initial_length + 1
    
    print(f"✓ New chain length: {len(node.blockchain.chain)}")
    print(f"✓ Block hash: {block.hash}")
    
    print("✅ TEST 5 PASSED\n")


def run_all_tests():
    """Chạy tất cả tests"""
    print("\n" + "="*80)
    print("🧪 RUNNING ALL TESTS")
    print("="*80)
    
    try:
        test_blockchain_basic()
        test_user_management()
        test_network()
        test_transaction_broadcast()
        test_mining()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED!")
        print("="*80)
        print("\nHệ thống hoạt động tốt! Có thể chạy main.py")
        print("="*80 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
