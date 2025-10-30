# Transaction Between Nodes - Hướng Dẫn

## 🐛 **Vấn đề: Transaction không broadcast được**

### **Triệu chứng:**
```
Node A tạo transaction → Node B
✅ Node A: Transaction in pending (1 transaction)
❌ Node B: No pending transactions (0 transactions)
❌ Node C: No pending transactions (0 transactions)
```

### **Nguyên nhân:**

Mỗi node có **blockchain riêng biệt**:

```
Node A: [Genesis] → [Block 1] → [Block 2] → [Block 3]
        A có 30 coins từ mining reward

Node B: [Genesis] → [Block 1]
        ❌ Blockchain của B KHÔNG có thông tin A có tiền!

Node C: [Genesis] → [Block 1] → [Block 2]
        ❌ Blockchain của C KHÔNG có thông tin A có tiền!
```

Khi A broadcast transaction:
1. Node A gửi POST `/transaction/new` đến B và C
2. Node B validate: `blockchain.add_transaction(tx)`
3. ❌ **Validation FAIL**: "Insufficient balance" 
   - Vì blockchain của B không biết A có balance
4. Transaction bị reject với HTTP 400

---

## ✅ **Giải pháp: Đồng bộ Blockchain trước khi giao dịch**

### **Quy trình đúng:**

```
BƯỚC 1: Sync Blockchain
┌─────────────────────────────────────────────────────────┐
│ Tất cả nodes phải có CÙNG blockchain                    │
│ để biết balance của nhau                                │
└─────────────────────────────────────────────────────────┘

BƯỚC 2: Create Transaction
┌─────────────────────────────────────────────────────────┐
│ Tạo transaction sau khi đã sync                         │
│ Validation sẽ pass vì đã có thông tin balance           │
└─────────────────────────────────────────────────────────┘

BƯỚC 3: Mine Block
┌─────────────────────────────────────────────────────────┐
│ Bất kỳ node nào cũng có thể mine                        │
│ vì đều có transaction trong pending                     │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 **Hướng dẫn chi tiết:**

### **Scenario: Node A gửi tiền cho Node B**

#### **Terminal 1 (Node A):**
```
python main.py

Login as: Alice
Password: ***

Main Menu:
  13. Synchronize blockchain    <-- 1️⃣ SYNC TRƯỚC!
  
🔄 Synchronizing blockchain with peers...
✅ Blockchain updated with longer chain from peers!

Main Menu:
  8. Check balance
  
💰 Your confirmed balance: 30 coins    <-- Có tiền

Main Menu:
  6. Create transaction
  
Receiver address: Bob
Amount: 10

✅ Transaction created and broadcasted!
📤 Alice → Bob: 10.0 coins
```

#### **Terminal 2 (Node B):**
```
python main.py

Login as: Bob
Password: ***

Main Menu:
  13. Synchronize blockchain    <-- 1️⃣ SYNC TRƯỚC!
  
🔄 Synchronizing blockchain with peers...
✅ Your blockchain is up to date!

Main Menu:
  8. Check balance
  
💰 Your confirmed balance: 10 coins
⏳ Pending Balance: +10 coins      <-- Nhận được transaction!
💡 You have 1 pending transaction(s)

Main Menu:
  7. Mine block                   <-- 2️⃣ MINE BLOCK
  
⛏️ Mining with difficulty 2...
✅ Block mined successfully!

Main Menu:
  8. Check balance
  
💰 Your confirmed balance: 30 coins   <-- 10 (ban đầu) + 10 (nhận) + 10 (reward)
```

#### **Terminal 3 (Node C):**
```
python main.py

Login as: Charlie
Password: ***

Main Menu:
  13. Synchronize blockchain    <-- 1️⃣ SYNC TRƯỚC!
  
🔄 Synchronizing blockchain with peers...
✅ Blockchain updated!

Main Menu:
  7. Mine block
  
⛏️ Mining...
💡 You have 1 pending transaction(s)  <-- Cũng có transaction!

✅ Block mined successfully!
```

---

## 🔍 **Kiểm tra Transaction có broadcast không:**

### **Trước khi sync:**
```
Node A:
  8. Check balance → 30 coins
  6. Create transaction → Bob, 10 coins
  ✅ Transaction created
  
Node B:
  8. Check balance → 
  ⏳ Pending: 0 coins
  ❌ KHÔNG có transaction!
```

### **Sau khi sync:**
```
ALL NODES:
  13. Synchronize blockchain
  ✅ All nodes have identical blockchain
  
Node A:
  6. Create transaction → Bob, 10 coins
  ✅ Transaction created and broadcasted
  
Node B:
  8. Check balance → 
  ⏳ Pending: +10 coins
  ✅ CÓ transaction!
  💡 You have 1 pending transaction(s)
```

---

## 💡 **Best Practices:**

### **1. Luôn sync trước khi tạo transaction:**
```
Menu option 13: Synchronize blockchain
→ Sau đó mới:
Menu option 6: Create transaction
```

### **2. Sync định kỳ khi có hoạt động:**
```
- Khi login vào node
- Trước khi tạo transaction
- Trước khi mine block
- Sau khi nhận block mới từ peer
```

### **3. Check pending transactions trước khi mine:**
```
Menu option 8: Check balance
→ Xem: "You have X pending transaction(s)"
→ Nếu có pending → Menu option 7: Mine block
```

---

## 🎯 **Workflow hoàn chỉnh:**

```
[Setup 3 nodes]
Terminal 1: python main.py → Login as Alice
Terminal 2: python main.py → Login as Bob  
Terminal 3: python main.py → Login as Charlie

↓

[Connect nodes]
All terminals → Option 11: Connect to peers
All terminals → Option 12: View network status
✅ Check: All nodes see each other

↓

[Sync blockchain]
All terminals → Option 13: Synchronize blockchain
✅ Check: All nodes have same chain length

↓

[Mine initial blocks (get funds)]
Terminal 1 (Alice) → Option 7: Mine block (x3)
✅ Alice now has 30 coins

↓

[Sync again]
All terminals → Option 13: Synchronize blockchain
✅ Now Bob & Charlie know Alice has 30 coins

↓

[Create transaction]
Terminal 1 (Alice) → Option 6: Create transaction
Receiver: Bob
Amount: 10
✅ Transaction broadcasted

↓

[Check pending]
Terminal 2 (Bob) → Option 8: Check balance
✅ Shows: "1 pending transaction(s)"

Terminal 3 (Charlie) → Option 8: Check balance
✅ Shows: "1 pending transaction(s)"

↓

[Mine transaction]
Terminal 2 (Bob) → Option 7: Mine block
✅ Block mined! Bob gets 20 coins (10 + 10 reward)

↓

[Sync final]
All terminals → Option 13: Synchronize blockchain
✅ All nodes have the new block
```

---

## 🚨 **Troubleshooting:**

### **Problem 1: "No pending transactions to mine"**
```
Nguyên nhân: Chưa sync blockchain trước khi tạo transaction
Giải pháp: 
  1. Option 13: Synchronize blockchain (tất cả nodes)
  2. Option 6: Create transaction (từ node gửi)
  3. Option 8: Check balance (node nhận → xem pending)
```

### **Problem 2: "Transaction validation failed"**
```
Nguyên nhân: Node nhận không biết node gửi có balance
Giải pháp: Sync blockchain trước!
```

### **Problem 3: "Broadcasting to 0 peers"**
```
Nguyên nhân: Không có peers connected
Giải pháp: 
  1. Option 11: Connect to peers
  2. Option 12: View network status → Check peer count
```

---

## 📊 **Debug Commands:**

```bash
# Check if nodes are connected
Option 12: View network status
→ Check: "Peers: X/8"

# Check if blockchain is synced
Option 5: View blockchain
→ Compare chain lengths between nodes

# Check pending transactions
Option 8: Check balance
→ Look for: "You have X pending transaction(s)"
```

---

## ✨ **Tóm tắt:**

| Bước | Hành động | Menu Option | Kết quả |
|------|-----------|-------------|---------|
| 1 | Connect nodes | 11 | Peers: 2/8 |
| 2 | **SYNC blockchain** | **13** | ✅ Same chain |
| 3 | Mine for funds | 7 | +10 coins |
| 4 | **SYNC again** | **13** | ✅ Others know balance |
| 5 | Create transaction | 6 | Transaction broadcast |
| 6 | Check pending | 8 | 1 pending transaction |
| 7 | Mine block | 7 | Transaction confirmed |
| 8 | Sync final | 13 | All nodes updated |

**KEY POINT:** Luôn **SYNC trước, Transaction sau!** 🔑
