# 🚀 HƯỚNG DẪN NHANH - Blockchain Sybil Attack Demo

## ⚡ Khởi động nhanh (5 phút)

### Bước 1: Cài đặt
```powershell
pip install -r requirements.txt
```

### Bước 2: Kiểm tra hệ thống
```powershell
python test_system.py
```
Nếu thấy "✅ ALL TESTS PASSED!" → OK!

### Bước 3: Chạy chương trình
```powershell
python main.py
```

## 🎮 Demo nhanh

### Demo 1: Tạo tài khoản và giao dịch (3 phút)
```
1. Chọn 1 → Đăng ký
   Username: alice
   Password: 123
   → Nhận 100 coins ban đầu!

2. Chọn 2 → Đăng nhập
   Username: alice
   Password: 123
   → Node tự động tạo và join mạng!
   → Balance: 100 coins

3. Chọn 8 → Check balance
   → Xem số dư: 100 coins

4. Chọn 6 → Tạo giao dịch
   Receiver: bob
   Amount: 50
   → Transaction được broadcast!
   → Balance còn: 50 coins (pending)

5. Chọn 7 → Mine block
   → Block được mine, nhận 10 coins reward!
   → Balance: 50 + 10 = 60 coins (sau khi mine block tiếp)

6. Chọn 5 → View blockchain
   → Xem toàn bộ blockchain
```

### Demo 2: Sybil Attack (2 phút)
```
1. Đăng nhập với tài khoản bất kỳ

2. Chọn 14 → Demonstrate Sybil Attack

3. Confirm "yes"
   → Hệ thống tạo 20 Sybil nodes
   → Phân tích mức độ kiểm soát mạng

4. Quan sát:
   - Network size tăng đột biến
   - Sybil nodes chiếm >50% mạng
   - Có thể manipulate consensus

5. Cleanup "yes"
   → Xóa tất cả Sybil nodes
```

### Demo 3: Eclipse Attack (2 phút)
```
1. Đăng nhập với tài khoản bất kỳ

2. Chọn 11 → Connect to peers
   → Kết nối với một số peers

3. Chọn 15 → Demonstrate Eclipse Attack

4. Confirm "yes"
   → Target node (bạn) bị isolate
   → Tất cả connections bị kiểm soát

5. Quan sát:
   - Node của bạn bị cô lập
   - Chỉ kết nối với malicious nodes
   - Nhận fake blockchain data

6. Cleanup "yes"
   → Restore connections bình thường
```

## 📚 Chạy Examples

### Example 1: Blockchain cơ bản
```powershell
python examples\example1_basic_blockchain.py
```
Học: Block, Transaction, Mining, Validation

### Example 2: P2P Network
```powershell
python examples\example2_p2p_network.py
```
Học: Nodes, Peers, Broadcasting, Synchronization

### Example 3: Sybil Attack
```powershell
python examples\example3_sybil_attack.py
```
Học: Network takeover, Attack metrics

### Example 4: Eclipse Attack
```powershell
python examples\example4_eclipse_attack.py
```
Học: Node isolation, False data injection

## 🎯 Menu chính

```
📋 Account (1-4):
  1. Register      → Đăng ký tài khoản mới
  2. Login         → Đăng nhập
  3. Logout        → Đăng xuất
  4. List accounts → Xem tất cả tài khoản

💼 Blockchain (5-9):
  5. View blockchain    → Xem chain
  6. Create transaction → Tạo giao dịch
  7. Mine block        → Mine block mới
  8. Check balance     → Kiểm tra số dư
  9. Validate          → Validate chain

🌐 Network (10-13):
  10. View node info   → Thông tin node
  11. Connect peers    → Kết nối peers
  12. Network status   → Trạng thái mạng
  13. Sync blockchain  → Đồng bộ chain

⚔️ Attacks (14-15):
  14. Sybil Attack    → Demo Sybil
  15. Eclipse Attack  → Demo Eclipse
```

## ⚙️ Cấu hình

Sửa `config.py`:

```python
DIFFICULTY = 4              # Độ khó mining (2-6)
MINING_REWARD = 10.0        # Coin/block
MAX_PEERS = 8               # Peers tối đa
SYBIL_NODES_COUNT = 20      # Số Sybil nodes
```

**Tips:**
- Giảm `DIFFICULTY` nếu mining quá lâu
- Tăng `SYBIL_NODES_COUNT` để attack mạnh hơn

## 🐛 Troubleshooting

| Lỗi | Fix |
|-----|-----|
| Port đã dùng | Tắt chương trình khác |
| Mining lâu | Giảm DIFFICULTY = 2 |
| Không connect | Check firewall |
| Import error | pip install -r requirements.txt |

## 📖 Tài liệu

- **README.md** - Overview
- **USER_GUIDE.md** - Hướng dẫn chi tiết
- **TECHNICAL_DETAILS.md** - Chi tiết kỹ thuật
- **GETTING_STARTED.md** - Getting started đầy đủ
- **examples/README.md** - Hướng dẫn examples

## 💡 Tips học tập

### 1. Học tuần tự
```
Tests → Example 1 → Example 2 → Example 3 → Example 4 → Main
```

### 2. Thực hành
- Chạy mỗi example 2-3 lần
- Thay đổi parameters
- Quan sát kết quả khác nhau

### 3. Hiểu code
- Đọc comments trong code
- Đọc TECHNICAL_DETAILS.md
- Debug với print statements

### 4. Thử nghiệm
- Tạo nhiều accounts
- Test với nhiều nodes
- Thử các attack scenarios

## 🎓 Kiến thức học được

### Blockchain
- ✅ Block structure và linking
- ✅ Proof of Work
- ✅ Transaction lifecycle
- ✅ Chain validation
- ✅ Consensus mechanisms

### P2P Network
- ✅ Node discovery
- ✅ Peer connections
- ✅ Broadcasting
- ✅ Synchronization

### Security
- ✅ Sybil Attack
- ✅ Eclipse Attack
- ✅ 51% Attack risks
- ✅ Double-spending
- ✅ Countermeasures

## 🚀 Workflow học tập đề xuất

### Ngày 1: Basics
1. Chạy test_system.py
2. Chạy example1 (blockchain basics)
3. Chạy example2 (networking)
4. Đọc TECHNICAL_DETAILS.md phần Core

### Ngày 2: Network
1. Tạo 3-4 accounts trong main.py
2. Thử transaction giữa các accounts
3. Thử mining và check balances
4. Đọc TECHNICAL_DETAILS.md phần Network

### Ngày 3: Attacks
1. Chạy example3 (Sybil attack)
2. Chạy example4 (Eclipse attack)
3. Demo attacks trong main.py
4. Đọc TECHNICAL_DETAILS.md phần Attack

### Ngày 4: Deep dive
1. Đọc toàn bộ source code
2. Thử modify code
3. Tạo scenarios riêng
4. Experiment!

## 🎉 Bắt đầu ngay!

```powershell
# Bắt đầu với main system
python main.py

# Hoặc bắt đầu với examples
python examples\example1_basic_blockchain.py
```

**Chúc bạn học tập vui vẻ!** 🎓🚀

---

## ❓ Câu hỏi thường gặp

**Q: Mining mất bao lâu?**  
A: 10-30 giây với DIFFICULTY=4

**Q: Tối đa bao nhiêu nodes?**  
A: Không giới hạn, nhưng nhiều nodes = chậm hơn

**Q: Transaction có phí không?**  
A: Không, đây là version đơn giản

**Q: Có thể undo transaction?**  
A: Không, blockchain immutable

**Q: Balance ban đầu là bao nhiêu?**  
A: **100 coins** khi đăng ký! (có thể thay đổi trong config.py)

**Q: Balance được lưu ở đâu?**  
A: Không lưu riêng! Balance được **tính động** từ toàn bộ blockchain history

**Q: Làm sao để có nhiều coins hơn?**  
A: Mine blocks để nhận rewards (10 coins/block)

**Q: Tại sao balance âm?**  
A: Không thể! Hệ thống check balance trước khi cho phép giao dịch

**Q: Xem chi tiết về balance?**  
A: Đọc file `BALANCE_SYSTEM.md`

---

**Sẵn sàng để khám phá blockchain security!** 🔐💪
