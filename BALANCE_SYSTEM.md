# Balance System - Hướng dẫn chi tiết

## 📊 Cách hoạt động của Balance

### 1. Initial Balance
Khi một user đăng ký, họ nhận **100 coins** ban đầu thông qua genesis block:

```python
# Trong config.py
INITIAL_BALANCE = 100.0  # Số dư ban đầu cho mỗi user mới
```

### 2. Balance được tính động

**QUAN TRỌNG**: Balance **KHÔNG được lưu trữ riêng**. Thay vào đó, nó được **tính toán động** từ toàn bộ blockchain:

```python
def get_balance(self, address):
    balance = 0
    
    # Duyệt qua tất cả blocks
    for block in self.chain:
        if block.transaction:
            # Trừ nếu là sender
            if block.transaction.sender == address:
                balance -= block.transaction.amount
            # Cộng nếu là receiver
            if block.transaction.receiver == address:
                balance += block.transaction.amount
    
    # Cộng/trừ pending transactions
    for tx in self.pending_transactions:
        if tx.sender == address:
            balance -= tx.amount
        if tx.receiver == address:
            balance += tx.amount
    
    return balance
```

## 💰 Nguồn gốc của coins

### 1. Initial Balance (100 coins)
Khi user đăng ký, genesis block tạo coinbase transaction:

```
Block #0 (Genesis):
  Transaction: System → Alice (100 coins)
  
Alice's balance = 100 coins
```

### 2. Mining Rewards (10 coins/block)
Khi mine block, miner nhận reward:

```
Alice mines block #1:
  → Pending transaction: System → Alice (10 coins)
  
Sau khi mine block #2 (để confirm reward):
  Alice's balance = 110 coins
```

### 3. P2P Transactions
Giao dịch giữa các users:

```
Alice → Bob (50 coins):
  Alice's balance = 110 - 50 = 60 coins
  Bob's balance = 0 + 50 = 50 coins
```

## 🔍 Kiểm tra Balance

### Trong main.py
```
Option 8: Check balance
→ Hiển thị balance hiện tại của node
```

### Trong code
```python
# Kiểm tra balance của một address
balance = blockchain.get_balance("Alice")
print(f"Alice's balance: {balance} coins")
```

## 📝 Ví dụ Flow đầy đủ

### User mới: Alice

```
1. Đăng ký:
   → Genesis block tạo: System → Alice (100 coins)
   → Alice's balance = 100 coins

2. Tạo transaction:
   → Alice → Bob (50 coins)
   → Pending transaction created
   → Alice's balance = 100 - 50 = 50 coins (tạm thời)

3. Mine block:
   → Alice mines block #1
   → Transaction confirmed
   → Mining reward pending: System → Alice (10 coins)
   → Alice's balance = 50 coins (chưa có reward)

4. Mine block tiếp:
   → Bob mines block #2
   → Mining reward của Alice confirmed
   → Alice's balance = 50 + 10 = 60 coins
```

## ⚠️ Lưu ý quan trọng

### 1. Không có double-spending
Balance được check trước khi tạo transaction:

```python
def create_transaction(self, receiver, amount):
    # Kiểm tra số dư
    balance = self.get_balance()
    if balance < amount:
        print(f"❌ Insufficient balance! Your balance: {balance} coins")
        return None
    
    # Tạo transaction
    transaction = Transaction(sender=self.username, receiver=receiver, amount=amount)
    self.blockchain.add_transaction(transaction)
```

### 2. Mining reward cần confirm
Mining reward là một transaction, nên cần được mine trong block tiếp theo mới có hiệu lực.

### 3. Balance calculation có thể chậm
Với blockchain dài, việc tính balance có thể chậm vì phải duyệt toàn bộ chain.

**Giải pháp tốt hơn (cho production)**:
- Cache balance trong memory
- Sử dụng UTXO model (như Bitcoin)
- Database indexing

## 🎯 Best Practices

### 1. Luôn check balance trước khi giao dịch
```python
balance = node.get_balance()
if balance >= amount:
    node.create_transaction(receiver, amount)
else:
    print("Not enough balance!")
```

### 2. Mine để có coins ban đầu
```python
# Nếu muốn có nhiều coins hơn
for i in range(5):
    # Tạo dummy transaction
    node.create_transaction("dummy", 0.1)
    # Mine
    node.mine_block()
```

### 3. Kiểm tra pending transactions
```python
# Balance bao gồm cả pending transactions
current_balance = blockchain.get_balance(address)

# Balance chỉ từ confirmed blocks
confirmed_balance = sum(
    block.transaction.amount 
    for block in blockchain.chain 
    if block.transaction.receiver == address
) - sum(
    block.transaction.amount 
    for block in blockchain.chain 
    if block.transaction.sender == address
)
```

## 🔧 Customize Initial Balance

Thay đổi trong `config.py`:

```python
# Nhiều coins hơn cho test
INITIAL_BALANCE = 1000.0

# Ít coins hơn để demo mining
INITIAL_BALANCE = 10.0

# Không có initial balance (phải mine)
INITIAL_BALANCE = 0.0
```

## 📊 Tracking Balance Changes

### Xem history của một address:

```python
def get_balance_history(blockchain, address):
    history = []
    balance = 0
    
    for i, block in enumerate(blockchain.chain):
        if block.transaction:
            if block.transaction.sender == address:
                balance -= block.transaction.amount
                history.append({
                    'block': i,
                    'type': 'sent',
                    'amount': -block.transaction.amount,
                    'balance': balance
                })
            
            if block.transaction.receiver == address:
                balance += block.transaction.amount
                history.append({
                    'block': i,
                    'type': 'received',
                    'amount': block.transaction.amount,
                    'balance': balance
                })
    
    return history

# Usage
history = get_balance_history(blockchain, "Alice")
for item in history:
    print(f"Block #{item['block']}: {item['type']} {item['amount']} → Balance: {item['balance']}")
```

## 🎓 Kết luận

- ✅ Initial balance: 100 coins (có thể thay đổi)
- ✅ Balance tính động từ blockchain
- ✅ Mining reward: 10 coins/block
- ✅ Check balance trước khi giao dịch
- ✅ Không lưu trữ riêng, tính từ history

**Hệ thống balance đã hoàn chỉnh và sẵn sàng sử dụng!** 💰✨
