# Examples - Blockchain Sybil Attack Demo

Thư mục này chứa các example scripts để demo các tính năng của hệ thống.

## Danh sách Examples

### Example 1: Basic Blockchain Operations
**File:** `example1_basic_blockchain.py`

Demo các tính năng cơ bản của blockchain:
- Tạo blockchain với genesis block
- Thêm transactions
- Mine blocks với Proof of Work
- Kiểm tra balances
- Validate blockchain

**Chạy:**
```powershell
python examples\example1_basic_blockchain.py
```

**Học được:**
- Cấu trúc blockchain
- Transaction lifecycle
- Mining process
- Balance tracking
- Chain validation

---

### Example 2: P2P Network Setup
**File:** `example2_p2p_network.py`

Demo thiết lập mạng P2P:
- Tạo nhiều nodes
- Kết nối nodes với nhau
- Broadcast transactions
- Network topology
- Node synchronization

**Chạy:**
```powershell
python examples\example2_p2p_network.py
```

**Học được:**
- P2P networking
- Peer connections
- Transaction broadcasting
- Network management
- Multi-node operations

---

### Example 3: Sybil Attack Simulation
**File:** `example3_sybil_attack.py`

Demo Sybil Attack đầy đủ:
- Setup honest network (5 nodes)
- Create Sybil nodes (15 nodes)
- Connect Sybil nodes
- Analyze network control
- Demonstrate attack capabilities
- Network visualization

**Chạy:**
```powershell
python examples\example3_sybil_attack.py
```

**Học được:**
- Cách Sybil attack hoạt động
- Network takeover strategies
- Attack success metrics
- Impact on consensus
- Countermeasures

---

### Example 4: Eclipse Attack Simulation
**File:** `example4_eclipse_attack.py`

Demo Eclipse Attack đầy đủ:
- Setup network with target
- Create malicious nodes
- Isolate target node
- Control all connections
- Feed false blockchain
- Demonstrate double-spending risk

**Chạy:**
```powershell
python examples\example4_eclipse_attack.py
```

**Học được:**
- Cách Eclipse attack hoạt động
- Node isolation techniques
- False information injection
- Impact on victim node
- Detection and prevention

---

## Hướng dẫn sử dụng

### 1. Chạy tất cả examples theo thứ tự
Để hiểu đầy đủ hệ thống, nên chạy theo thứ tự:
1. Example 1 (Blockchain basics)
2. Example 2 (Networking)
3. Example 3 (Sybil attack)
4. Example 4 (Eclipse attack)

### 2. Interactive mode
Hầu hết examples có các điểm dừng để bạn quan sát:
- Đọc output cẩn thận
- Press Enter khi prompted
- Quan sát network state changes

### 3. Modify và experiment
Bạn có thể chỉnh sửa examples:
- Thay đổi số lượng nodes
- Thay đổi transaction amounts
- Thay đổi network topology
- Test different attack scenarios

## Tips

### Chạy example với verbose output
```powershell
python examples\example1_basic_blockchain.py 2>&1 | Tee-Object -FilePath output.log
```

### So sánh nhiều runs
Chạy example nhiều lần với parameters khác nhau để thấy sự khác biệt.

### Kết hợp với visualization
Examples đã tích hợp visualization để dễ hiểu hơn.

### Debug mode
Thêm print statements để debug:
```python
print(f"Debug: {variable}")
```

## Troubleshooting

**Q: Example bị lỗi port?**  
A: Đóng các instance khác hoặc đợi port release.

**Q: Mining quá lâu?**  
A: Giảm DIFFICULTY trong config.py.

**Q: Nodes không kết nối?**  
A: Kiểm tra firewall settings.

**Q: Output quá nhiều?**  
A: Redirect output: `> output.txt`

## Next Steps

Sau khi chạy hết examples:
1. Chạy `main.py` để interactive mode
2. Tự tạo scenarios riêng
3. Modify code để test ideas
4. Đọc TECHNICAL_DETAILS.md để hiểu sâu hơn

## Learning Path

```
Example 1 (Basics)
    ↓
Example 2 (Networking)
    ↓
Example 3 (Sybil Attack)
    ↓
Example 4 (Eclipse Attack)
    ↓
main.py (Full System)
    ↓
Custom Experiments
```

Enjoy learning! 🎓🔗
