# Eclipse Attack - Complete Guide

## 📖 Tổng Quan

Eclipse Attack là một cuộc tấn công mạng P2P trong đó kẻ tấn công cô lập node mục tiêu bằng cách kiểm soát tất cả các kết nối của nó. Điều này cho phép tấn công double-spending thành công.

## 🎯 Mục Tiêu Demo

Demo này mô phỏng một cuộc tấn công Eclipse hoàn chỉnh với kịch bản double-spending thực tế:

1. **Tạo malicious nodes** - Tạo nhiều node độc hại
2. **Khởi động malicious network** - Start các node độc hại
3. **Chọn target** - Chọn node nạn nhân từ mạng
4. **Eclipse attack** - Cô lập target bằng cách lấp đầy MAX_PEERS slots
5. **Double-spending** - Thực hiện chi tiêu gấp đôi
6. **Cleanup** - Dọn dẹp tất cả흔적

## 🔧 Yêu Cầu

- Python 3.7+
- Flask
- Requests
- Ít nhất 1 legitimate node đang chạy trong network

## 🚀 Cách Sử Dụng

### Bước 1: Chuẩn Bị

```bash
# Đảm bảo có ít nhất 1 legitimate node
# Terminal 1: Start legitimate node
python main.py
# Login với account thường (VD: Alice, Bob)
```

### Bước 2: Chạy Demo

```bash
# Terminal 2: Run Eclipse Attack Demo
python demo_eclipse_attack.py
```

### Bước 3: Theo Dõi Demo

Demo sẽ thực hiện 6 bước:

#### **STEP 1: CREATE MALICIOUS ACCOUNTS**
- Nhập số lượng malicious nodes (khuyến nghị: 8)
- Script tự động tạo accounts: `Malicious_001`, `Malicious_002`, ...
- Mỗi account được đăng ký thật trong hệ thống

#### **STEP 2: START MALICIOUS NODES**
- Khởi động Flask server cho mỗi node
- Load blockchain data
- Các node bắt đầu lắng nghe trên ports 5001, 5002, ...

#### **STEP 3: SELECT TARGET**
- Hiển thị danh sách legitimate nodes trong network
- Chọn node mục tiêu (nạn nhân)

#### **STEP 4: ECLIPSE ATTACK**
**Phase 1: Cô lập target**
- Xác định các legitimate nodes trong mạng
- Ngăn target kết nối với legitimate nodes

**Phase 2: Lấp đầy connection slots**
- Kết nối tối đa 8 malicious nodes tới target (MAX_PEERS = 8)
- Target bị cô lập hoàn toàn, chỉ kết nối với malicious nodes

#### **STEP 5: DOUBLE-SPENDING ATTACK**

**Phase 1: Gửi tiền cho Target (Eclipse Network)**
```
Attacker → Target (50 coins)
       ↓
Malicious nodes mine block
       ↓
Broadcast block to Target
       ↓
Target nhận +50 coins ✓
```

**Phase 2: Gửi cùng số tiền cho Malicious Node (Legitimate Network)**
```
Attacker → Malicious_002 (50 coins) [SAME COINS!]
       ↓
Broadcast to legitimate nodes
       ↓
Legitimate nodes mine block
       ↓
Legitimate chain dài hơn!
```

**Phase 3: Reconnect & Sync**
```
Shutdown malicious nodes
       ↓
Target reconnects to legitimate network
       ↓
Target syncs with longer legitimate chain
       ↓
Target's transaction REVERTED! ❌
Target mất 50 coins!
```

#### **STEP 6: CLEANUP**
- Xóa tất cả malicious accounts
- Dọn dẹp network registry
- Hệ thống trở về trạng thái ban đầu

## 📊 Kết Quả Mong Đợi

### Trước Tấn Công
```
Target balance: 100 coins
Network: 1 legitimate node + 8 malicious nodes
Target peers: Mixed (legitimate + malicious)
```

### Sau Eclipse
```
Target peers: 8 malicious nodes (100% isolated)
Legitimate nodes: Cannot connect (MAX_PEERS reached)
```

### Sau Double-Spending
```
Eclipse chain: Target +50 coins (from Attacker)
Legit chain:   Malicious_002 +50 coins (from Attacker)
```

### Sau Sync
```
Target balance: 100 coins (transaction reverted!)
Malicious_002: +50 coins (attack successful!)
Same coins spent TWICE!
```

## 🔍 Chi Tiết Kỹ Thuật

### 1. MAX_PEERS Limit

```python
# config.py
MAX_PEERS = 8  # Maximum connections per node
```

**Eclipse attack hoạt động vì:**
- Mỗi node chỉ chấp nhận tối đa 8 kết nối
- Attacker lấp đầy tất cả 8 slots bằng malicious nodes
- Legitimate nodes không thể kết nối (connection refused)

### 2. Connection Management

```python
# network/node.py - add_peer() method
if len(self.peers) >= config.MAX_PEERS:
    return False  # Reject new connection
```

### 3. Consensus Resolution

```python
# Target syncs with legitimate network
longest_chain = get_longest_chain_from_peers()
if len(longest_chain) > len(current_chain):
    replace_chain(longest_chain)  # Revert eclipse transactions
```

### 4. Double-Spending Logic

```
SAME INPUT (50 coins) → TWO OUTPUTS:
├─ Output 1: Target (eclipse chain)
└─ Output 2: Malicious_002 (legit chain)

Legit chain wins (longer) → Output 1 reverted!
```

## ⚠️ Lỗi Thường Gặp

### 1. No Legitimate Nodes
```
❌ No legitimate nodes found!
```
**Giải pháp:** Start ít nhất 1 legitimate node trước khi chạy demo

### 2. Connection Failed
```
❌ Failed to connect to target
```
**Giải pháp:** 
- Kiểm tra target node đang chạy
- Kiểm tra firewall/ports
- Thử lại với target khác

### 3. MAX_PEERS Not Filled
```
⚠️ Only 5/8 connections established
```
**Giải pháp:**
- Tạo thêm malicious nodes (>8)
- Kiểm tra network connectivity
- Đảm bảo ports không bị conflict

### 4. Sync Failed
```
❌ Target did not sync with legitimate network
```
**Giải pháp:**
- Đợi malicious nodes shutdown hoàn toàn
- Manually trigger sync trên target: `/sync` endpoint
- Kiểm tra legitimate nodes có chain dài hơn

## 🛡️ Phòng Chống Eclipse Attack

### 1. Increase MAX_PEERS
```python
MAX_PEERS = 50  # Harder to eclipse with more connections
```

### 2. Diversify Connections
- Kết nối với nhiều subnets khác nhau
- Ưu tiên trusted nodes
- Random peer selection

### 3. Monitor Peer Changes
```python
if new_peer_rate > threshold:
    alert("Possible eclipse attack!")
```

### 4. Checkpoint System
```python
# Accept only chains passing through known checkpoints
if not chain.has_valid_checkpoints():
    reject()
```

### 5. Peer Reputation
```python
# Prioritize long-standing peers
peer_score = connection_duration * successful_blocks
```

## 📈 Attack Success Metrics

**Eclipse Attack Success:**
- ✅ Target isolated (100% malicious peers)
- ✅ Legitimate nodes blocked
- ✅ Target accepts fake transactions

**Double-Spending Success:**
- ✅ Transaction confirmed on eclipse chain
- ✅ Same coins spent on legitimate chain
- ✅ Target loses money after sync

## 🎓 Học Từ Demo

1. **Network Layer is Critical**
   - P2P topology security is as important as consensus
   - Connection limits can be exploited

2. **Consensus is Not Enough**
   - Even with correct consensus, network isolation breaks security
   - Need both: secure consensus + secure network

3. **Real-World Implications**
   - Merchants accepting 0-conf transactions are vulnerable
   - Need multiple confirmations from diverse sources
   - SPV wallets particularly vulnerable

4. **Defense in Depth**
   - No single defense is sufficient
   - Combine multiple strategies
   - Monitor network behavior continuously

## 📚 Tham Khảo

- **Bitcoin Eclipse Attacks**: https://eprint.iacr.org/2015/263.pdf
- **Ethereum Eclipse Attacks**: https://www.usenix.org/system/files/sec20-zhou-zhiqiang.pdf
- **P2P Network Security**: https://en.wikipedia.org/wiki/Eclipse_attack

## 🔗 Liên Quan

- `BALANCE_FIX.md` - Balance calculation system
- `TRANSACTION_SYNC_FIX.md` - Transaction propagation
- `cleanup.py` - System cleanup utility
- `config.py` - Network parameters

## 👤 Tác Giả

Demo được tạo để minh họa rõ ràng cách Eclipse Attack hoạt động và tại sao nó nguy hiểm trong blockchain P2P networks.

---

**⚠️ CẢNH BÁO:** Demo này chỉ để giáo dục. KHÔNG sử dụng trên production networks hoặc với ý định xấu.
