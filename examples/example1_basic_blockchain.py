"""
Example 1: Basic blockchain operations
Demonstrates creating blockchain, transactions, and mining
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.blockchain import Blockchain
from core.transaction import Transaction


def main():
    print("\n" + "="*80)
    print("EXAMPLE 1: BASIC BLOCKCHAIN OPERATIONS")
    print("="*80)
    
    # 1. Tạo blockchain
    print("\n1. Creating blockchain for Alice...")
    blockchain = Blockchain(owner_address="Alice")
    print(f"✓ Genesis block created")
    print(f"   Chain length: {len(blockchain.chain)}")
    print(f"   Alice's initial balance: {blockchain.get_balance('Alice')} coins")
    
    # 2. Tạo transactions
    print("\n2. Creating transactions...")
    tx1 = Transaction("Alice", "Bob", 50)
    tx2 = Transaction("Bob", "Charlie", 30)
    
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    print(f"✓ Added 2 transactions")
    print(f"   Pending: {len(blockchain.pending_transactions)}")
    
    # 3. Mine block 1
    print("\n3. Mining block 1...")
    block1 = blockchain.mine_pending_transactions("Alice")
    print(f"✓ Block mined: {block1.hash[:20]}...")
    print(f"   Chain length: {len(blockchain.chain)}")
    
    # 4. Mine block 2 (mining reward transaction)
    print("\n4. Mining block 2...")
    block2 = blockchain.mine_pending_transactions("Bob")
    print(f"✓ Block mined: {block2.hash[:20]}...")
    print(f"   Chain length: {len(blockchain.chain)}")
    
    # 5. Check balances
    print("\n5. Checking balances...")
    alice_balance = blockchain.get_balance("Alice")
    bob_balance = blockchain.get_balance("Bob")
    charlie_balance = blockchain.get_balance("Charlie")
    
    print(f"✓ Alice:   {alice_balance:>6.1f} coins")
    print(f"✓ Bob:     {bob_balance:>6.1f} coins")
    print(f"✓ Charlie: {charlie_balance:>6.1f} coins")
    
    # 6. Validate chain
    print("\n6. Validating blockchain...")
    is_valid = blockchain.is_chain_valid()
    print(f"✓ Chain is valid: {is_valid}")
    
    # 7. Display full chain
    print("\n7. Full blockchain:")
    blockchain.display_chain()
    
    print("\n" + "="*80)
    print("✅ EXAMPLE 1 COMPLETED")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
