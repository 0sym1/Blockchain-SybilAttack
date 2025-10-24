# Hướng dẫn sử dụng - Blockchain Sybil Attack Demo

## Cài đặt

### Bước 1: Cài đặt Python dependencies
```powershell
pip install -r requirements.txt
```

### Bước 2: Chạy chương trình
```powershell
python main.py
```

## Hướng dẫn chi tiết

### 1. Đăng ký tài khoản

Chọn option `1` trong menu:
```
Enter username: alice
Enter password: 123456
```

- Username không được chứa khoảng trắng
- Mật khẩu không được mã hóa (chỉ demo)
- Tự động tạo Genesis block cho user mới

### 2. Đăng nhập

Chọn option `2`:
```
Enter username: alice
Enter password: 123456
```

Sau khi đăng nhập:
- Node tự động được tạo trên port khả dụng
- Tự động join vào mạng
- Tự động kết nối random tối đa 8 peers
- Load blockchain từ file account

### 3. Tạo giao dịch (P2P Transaction)

Chọn option `6`:
```
Receiver address: bob
Amount: 50
```

- Hệ thống kiểm tra số dư
- Transaction được broadcast đến tất cả peers
- Transaction vào pending pool

### 4. Mine block

Chọn option `7`:

- Mine transaction đầu tiên trong pending pool
- Sử dụng Proof of Work (độ khó = 4)
- Nhận mining reward (10 coins)
- Block được broadcast đến peers

### 5. Xem blockchain

Chọn option `5`:

Hiển thị toàn bộ chain:
- Block index
- Timestamp
- Previous hash
- Current hash
- Nonce
- Transaction details

### 6. Kết nối với peers

Chọn option `11`:

- Tự động tìm và kết nối peers ngẫu nhiên
- Tối đa 8 peers mỗi node
- Ping để kiểm tra kết nối

### 7. Đồng bộ blockchain

Chọn option `13`:

- Request blockchain từ tất cả peers
- So sánh độ dài chain
- Áp dụng longest chain rule
- Update chain nếu có chain dài hơn

### 8. Xem thông tin mạng

Chọn option `12`:

Hiển thị:
- Tổng số nodes trong mạng
- Trạng thái mỗi node (Active/Inactive)
- URL của từng node

## Demo tấn công

### Sybil Attack Demo

Chọn option `14`:

**Các bước:**
1. Tạo 20 Sybil nodes giả mạo
2. Kết nối các Sybil nodes với nhau
3. Phân tích tỷ lệ kiểm soát mạng
4. Demo khả năng tấn công

**Kết quả:**
- Sybil nodes chiếm >50% mạng
- Có thể manipulate consensus
- Có thể reject transactions
- Có thể eclipse honest nodes

**Cleanup:**
- Xóa tất cả Sybil nodes
- Khôi phục mạng bình thường

### Eclipse Attack Demo

Chọn option `15`:

**Lưu ý:** Cần đăng nhập trước (node của bạn sẽ là target)

**Các bước:**
1. Tạo 8 malicious nodes
2. Disconnect target khỏi honest peers
3. Connect target với tất cả malicious nodes
4. Feed fake blockchain cho target

**Kết quả:**
- Target bị cô lập hoàn toàn
- Tất cả connections bị kiểm soát
- Target nhận fake data
- Có thể thực hiện double-spending

**Cleanup:**
- Xóa malicious nodes
- Khôi phục connections bình thường

## Kịch bản thực hành

### Scenario 1: Giao dịch P2P đơn giản

1. Đăng ký 3 users: alice, bob, charlie
2. Login alice → tạo transaction cho bob (50 coins)
3. Login bob → mine block
4. Kiểm tra balance của alice và bob
5. Bob tạo transaction cho charlie (20 coins)
6. Charlie mine block
7. Xem blockchain của cả 3 nodes

### Scenario 2: Blockchain synchronization

1. Đăng ký 2 users: alice, bob
2. Login alice → tạo và mine 5 blocks
3. Logout alice
4. Login bob → bob có chain ngắn hơn
5. Synchronize blockchain → bob nhận chain của alice
6. Verify cả 2 có chain giống nhau

### Scenario 3: Sybil Attack

1. Tạo 5 honest users và login
2. Tạo giao dịch giữa các users
3. Chạy Sybil Attack demo (tạo 20 Sybil nodes)
4. Quan sát tỷ lệ Sybil/Honest nodes
5. Phân tích khả năng tấn công
6. Cleanup Sybil nodes

### Scenario 4: Eclipse Attack

1. Đăng ký alice và bob
2. Login alice (target)
3. Alice kết nối với several peers
4. Chạy Eclipse Attack demo
5. Quan sát alice bị isolate
6. Demo fake transactions
7. Cleanup và restore

### Scenario 5: 51% Attack (Advanced)

1. Tạo honest network với 10 nodes
2. Mỗi node mine blocks
3. Tạo 15 Sybil nodes (>50% mạng)
4. Sybil nodes tạo alternative chain
5. Sybil chain dài hơn → override honest chain
6. Demo double-spending attack

## Tips & Tricks

### Kiểm tra node info nhanh
```
Option 10: View node info
```

### Monitor pending transactions
```
Option 5: View blockchain
→ Xem số pending transactions
```

### Test blockchain validity
```
Option 9: Validate blockchain
→ Check hash integrity
```

### Xem network overview
```
Option 12: View network status
→ List tất cả nodes
```

### Force resync nếu out of sync
```
Option 13: Synchronize blockchain
→ Update với longest chain
```

## Troubleshooting

### Lỗi: Port already in use
- Đóng các instance khác của chương trình
- Hoặc đợi port được release

### Lỗi: Cannot connect to peers
- Kiểm tra peers có đang chạy không
- Check firewall settings
- Thử reconnect (Option 11)

### Lỗi: Chain validation failed
- Có thể do attack hoặc corruption
- Thử sync với peers (Option 13)
- Worst case: logout và login lại

### Lỗi: Mining quá lâu
- Giảm DIFFICULTY trong config.py
- Normal: 10-30 giây với DIFFICULTY=4

### Node không nhận được blocks
- Kiểm tra peer connections
- Synchronize blockchain
- Reconnect to peers

## Best Practices

1. **Luôn mine block sau khi tạo transaction** để transaction được confirm
2. **Sync blockchain định kỳ** nếu node offline một thời gian
3. **Maintain peer connections** - reconnect nếu số peers giảm
4. **Validate blockchain** trước khi tin tưởng dữ liệu
5. **Logout properly** để save blockchain vào file
6. **Monitor network size** trước khi demo attack

## Câu hỏi thường gặp

**Q: Tại sao balance âm?**
A: Tạo transaction mà không đủ balance từ mining

**Q: Transaction không được confirm?**
A: Cần có người mine block để confirm transaction

**Q: Chain bị fork?**
A: Normal trong P2P network, consensus sẽ resolve

**Q: Làm sao biết attack thành công?**
A: Xem output của attack demo, có thống kê chi tiết

**Q: Có thể undo transaction?**
A: Không, blockchain immutable (trừ khi attack thành công)

**Q: Mining reward đi đâu?**
A: Vào pending transactions, cần mine block tiếp

## Kết luận

Project này giúp hiểu:
- Cơ chế blockchain cơ bản
- P2P networking
- Proof of Work mining
- Security vulnerabilities
- Attack vectors
- Countermeasures

Enjoy learning blockchain security! 🔐🔗
