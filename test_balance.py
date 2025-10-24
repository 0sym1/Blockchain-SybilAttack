"""
Test Balance Fix - Automated Testing
"""

from core.blockchain import Blockchain
from core.transaction import Transaction
from core.block import Block

def test_balance_confirmed_only():
    """Test 1: Balance chỉ tính confirmed transactions"""
    print("\n" + "="*80)
    print("TEST 1: Balance Calculation (Confirmed Only)")
    print("="*80)
    
    # Setup
    blockchain = Blockchain(owner_address="Alice")
    
    # Initial balance (from genesis)
    initial_balance = blockchain.get_balance("Alice")
    print(f"✅ Alice initial balance: {initial_balance} coins")
    assert initial_balance == 100, f"Expected 100, got {initial_balance}"
    
    # Create pending transaction
    tx = Transaction(sender="Alice", receiver="Bob", amount=50)
    blockchain.add_transaction(tx)
    
    # Check balance KHÔNG thay đổi (vì chưa mine)
    balance_after_pending = blockchain.get_balance("Alice")
    print(f"✅ Alice balance after pending tx: {balance_after_pending} coins")
    assert balance_after_pending == 100, f"Expected 100 (unchanged), got {balance_after_pending}"
    
    # Check pending balance
    pending = blockchain.get_pending_balance("Alice")
    print(f"✅ Alice pending balance: {pending} coins")
    assert pending == -50, f"Expected -50, got {pending}"
    
    # Mine transaction
    block = blockchain.mine_pending_transactions("Miner")
    
    # Check balance SAU khi mine
    balance_after_mine = blockchain.get_balance("Alice")
    print(f"✅ Alice balance after mining: {balance_after_mine} coins")
    assert balance_after_mine == 50, f"Expected 50, got {balance_after_mine}"
    
    # Check Bob received
    bob_balance = blockchain.get_balance("Bob")
    print(f"✅ Bob balance after mining: {bob_balance} coins")
    assert bob_balance == 50, f"Expected 50, got {bob_balance}"
    
    print("\n✅ TEST 1 PASSED!\n")


def test_double_spending_prevention():
    """Test 2: Ngăn chặn double-spending"""
    print("="*80)
    print("TEST 2: Double-Spending Prevention")
    print("="*80)
    
    # Setup
    blockchain = Blockchain(owner_address="Alice")
    
    # Alice có 100 coins
    print(f"✅ Alice initial: {blockchain.get_balance('Alice')} coins")
    
    # Transaction 1: Alice→Bob 60 coins
    tx1 = Transaction(sender="Alice", receiver="Bob", amount=60)
    blockchain.add_transaction(tx1)
    print(f"✅ Created tx1: Alice→Bob 60 coins")
    
    confirmed, pending, total = blockchain.get_total_balance("Alice")
    print(f"   Alice: Confirmed={confirmed}, Pending={pending}, Total={total}")
    
    # Transaction 2: Alice→Charlie 50 coins (should FAIL)
    try:
        tx2 = Transaction(sender="Alice", receiver="Charlie", amount=50)
        blockchain.add_transaction(tx2)
        print("❌ TEST 2 FAILED: Should have raised ValueError!")
        assert False, "Expected ValueError"
    except ValueError as e:
        print(f"✅ Correctly rejected tx2: {str(e)}")
    
    print("\n✅ TEST 2 PASSED!\n")


def test_negative_balance_prevention():
    """Test 3: Ngăn chặn negative balance"""
    print("="*80)
    print("TEST 3: Negative Balance Prevention")
    print("="*80)
    
    # Setup - Alice có 0 coins (no genesis)
    blockchain = Blockchain()  # No owner
    
    alice_balance = blockchain.get_balance("Alice")
    print(f"✅ Alice initial: {alice_balance} coins")
    
    # Try to send 10 coins
    try:
        tx = Transaction(sender="Alice", receiver="Bob", amount=10)
        blockchain.add_transaction(tx)
        print("❌ TEST 3 FAILED: Should have raised ValueError!")
        assert False, "Expected ValueError"
    except ValueError as e:
        print(f"✅ Correctly rejected: {str(e)}")
    
    print("\n✅ TEST 3 PASSED!\n")


def test_persistence_consistency():
    """Test 4: Balance consistency after save/load"""
    print("="*80)
    print("TEST 4: Persistence Consistency")
    print("="*80)
    
    # Create blockchain with transactions
    blockchain1 = Blockchain(owner_address="Alice")
    
    # Alice→Bob: 30 coins
    tx1 = Transaction(sender="Alice", receiver="Bob", amount=30)
    blockchain1.add_transaction(tx1)
    blockchain1.mine_pending_transactions("Miner")
    
    # Alice→Charlie: 20 coins
    tx2 = Transaction(sender="Alice", receiver="Charlie", amount=20)
    blockchain1.add_transaction(tx2)
    blockchain1.mine_pending_transactions("Miner")
    
    # Check balances before save
    alice_before = blockchain1.get_balance("Alice")
    bob_before = blockchain1.get_balance("Bob")
    charlie_before = blockchain1.get_balance("Charlie")
    
    print(f"Before save:")
    print(f"  Alice: {alice_before} coins")
    print(f"  Bob: {bob_before} coins")
    print(f"  Charlie: {charlie_before} coins")
    
    # Serialize
    chain_data = blockchain1.to_list()
    
    # Load into new blockchain
    blockchain2 = Blockchain.from_list(chain_data, owner_address="Alice")
    
    # Check balances after load
    alice_after = blockchain2.get_balance("Alice")
    bob_after = blockchain2.get_balance("Bob")
    charlie_after = blockchain2.get_balance("Charlie")
    
    print(f"\nAfter load:")
    print(f"  Alice: {alice_after} coins")
    print(f"  Bob: {bob_after} coins")
    print(f"  Charlie: {charlie_after} coins")
    
    # Verify consistency
    assert alice_before == alice_after, f"Alice balance mismatch: {alice_before} vs {alice_after}"
    assert bob_before == bob_after, f"Bob balance mismatch: {bob_before} vs {bob_after}"
    assert charlie_before == charlie_after, f"Charlie balance mismatch: {charlie_before} vs {charlie_after}"
    
    print("\n✅ TEST 4 PASSED!\n")


def test_mining_reward():
    """Test 5: Mining reward calculation"""
    print("="*80)
    print("TEST 5: Mining Reward")
    print("="*80)
    
    blockchain = Blockchain(owner_address="Alice")
    
    # Alice→Bob: 50
    tx = Transaction(sender="Alice", receiver="Bob", amount=50)
    blockchain.add_transaction(tx)
    
    # Bob mines
    print("Bob is mining...")
    blockchain.mine_pending_transactions("Bob")
    
    # Bob should have 50 (from transaction) confirmed
    # Mining reward is still pending
    bob_confirmed = blockchain.get_balance("Bob")
    bob_pending = blockchain.get_pending_balance("Bob")
    
    print(f"Bob after mining:")
    print(f"  Confirmed: {bob_confirmed} coins")
    print(f"  Pending: {bob_pending} coins")
    
    assert bob_confirmed == 50, f"Expected 50 confirmed, got {bob_confirmed}"
    assert bob_pending == 10, f"Expected 10 pending reward, got {bob_pending}"
    
    # Mine reward block
    blockchain.mine_pending_transactions("Miner")
    
    # Now Bob should have 60 confirmed
    bob_final = blockchain.get_balance("Bob")
    print(f"Bob after reward mined: {bob_final} coins")
    assert bob_final == 60, f"Expected 60, got {bob_final}"
    
    print("\n✅ TEST 5 PASSED!\n")


if __name__ == "__main__":
    print("\n" + "🧪"*40)
    print("AUTOMATED BALANCE FIX TESTING")
    print("🧪"*40)
    
    try:
        test_balance_confirmed_only()
        test_double_spending_prevention()
        test_negative_balance_prevention()
        test_persistence_consistency()
        test_mining_reward()
        
        print("\n" + "="*80)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("="*80)
        print("\n✅ Balance calculation: CORRECT")
        print("✅ Double-spending prevention: WORKING")
        print("✅ Negative balance prevention: WORKING")
        print("✅ Persistence consistency: WORKING")
        print("✅ Mining reward: WORKING")
        print("\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}\n")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
