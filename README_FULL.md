# Blockchain Sybil & Eclipse Attack Demo

## 🎯 Mục đích
Project này được xây dựng để demo và nghiên cứu các loại tấn công trong mạng blockchain P2P:
- **Sybil Attack**: Tạo nhiều node giả mạo để chiếm quyền kiểm soát mạng
- **Eclipse Attack**: Cô lập một node bằng cách kiểm soát tất cả kết nối của nó

## ⚠️ Cảnh báo
Đây là project **DEMO CHO MỤC ĐÍCH HỌC TẬP**. KHÔNG sử dụng trong môi trường production.

## 🚀 Cài đặt nhanh

### 1. Cài đặt dependencies
```powershell
pip install -r requirements.txt
```

### 2. Chạy tests (optional)
```powershell
python test_system.py
```

### 3. Chạy chương trình
```powershell
python main.py
```

## 📋 Tính năng chính

### Core Features
✅ Blockchain với Proof of Work  
✅ Peer-to-peer networking (max 8 peers/node)  
✅ Transaction pool & broadcasting  
✅ Automatic chain synchronization  
✅ User account system (file-based)  
✅ Mining với rewards  

### Attack Simulations
⚔️ **Sybil Attack**: Tạo 20+ node giả mạo chiếm >50% mạng  
⚔️ **Eclipse Attack**: Cô lập và kiểm soát hoàn toàn 1 target node  

## 📁 Cấu trúc Project

```
Blockchain-SybilAttack/
├── core/                   # Blockchain core logic
│   ├── block.py           # Block structure
│   ├── blockchain.py      # Blockchain management
│   ├── transaction.py     # Transaction structure
│   └── proof_of_work.py   # Mining algorithm
│
├── network/               # P2P networking
│   ├── node.py           # Node với Flask API
│   ├── network_manager.py # Network registry
│   └── peer_discovery.py  # Peer connection logic
│
├── auth/                  # User management
│   └── user_manager.py   # Register/Login system
│
├── attack/                # Attack simulators
│   ├── sybil_attack.py   # Sybil attack demo
│   └── eclipse_attack.py # Eclipse attack demo
│
├── accounts/              # User data (auto-created)
├── main.py               # Entry point
├── config.py             # Configuration
├── test_system.py        # System tests
└── requirements.txt      # Dependencies
```

## 🎮 Hướng dẫn sử dụng

### Menu chính
```
📋 Account Management:
  1. Register new account
  2. Login
  3. Logout
  4. List all accounts

💼 Blockchain Operations:
  5. View blockchain
  6. Create transaction
  7. Mine block
  8. Check balance
  9. Validate blockchain

🌐 Network Operations:
  10. View node info
  11. Connect to peers
  12. View network status
  13. Synchronize blockchain

⚔️ Attack Simulations:
  14. Demonstrate Sybil Attack
  15. Demonstrate Eclipse Attack
```

### Quick Start Example

1. **Đăng ký tài khoản**
```
Option 1 → Username: alice → Password: 123
```

2. **Đăng nhập**
```
Option 2 → Username: alice → Password: 123
→ Node tự động tạo và join network
```

3. **Tạo giao dịch**
```
Option 6 → Receiver: bob → Amount: 50
→ Transaction broadcast đến peers
```

4. **Mine block**
```
Option 7 → Mining...
→ Block confirmed, nhận 10 coins reward
```

5. **Demo Sybil Attack**
```
Option 14 → Yes
→ Tạo 20 Sybil nodes
→ Phân tích tỷ lệ kiểm soát mạng
```

## 🔧 Configuration

Chỉnh sửa `config.py`:

```python
DIFFICULTY = 4              # Độ khó mining (số lượng số 0 đầu hash)
MINING_REWARD = 10.0        # Phần thưởng mining
BASE_PORT = 5000            # Port bắt đầu cho nodes
MAX_PEERS = 8               # Số peers tối đa mỗi node
SYBIL_NODES_COUNT = 20      # Số Sybil nodes trong attack
ECLIPSE_MALICIOUS_NODES = 8 # Số malicious nodes để eclipse
```

## 🎓 Kiến thức học được

### Blockchain Basics
- Block structure với hash linking
- Proof of Work consensus
- Transaction lifecycle
- Chain validation
- Longest chain rule

### P2P Networking
- Node discovery
- Peer connection management
- Broadcasting protocols
- Network synchronization

### Security & Attacks
- **Sybil Attack**: Hiểu cách attacker tạo nhiều identities để chiếm mạng
- **Eclipse Attack**: Hiểu cách isolate nodes và feed fake data
- **51% Attack**: Khả năng khi chiếm >50% mạng
- **Double-spending**: Risk khi bị attack

### Countermeasures
- Proof of Work/Stake requirements
- Peer reputation systems
- Diverse peer selection
- Network monitoring

## 📚 Tài liệu

- [USER_GUIDE.md](USER_GUIDE.md) - Hướng dẫn chi tiết từng tính năng
- [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md) - Giải thích kỹ thuật chi tiết

## 🧪 Testing

Chạy test suite:
```powershell
python test_system.py
```

Tests bao gồm:
- ✅ Blockchain basic operations
- ✅ User management (register/login)
- ✅ Network operations
- ✅ Transaction broadcasting
- ✅ Mining functionality

## 💡 Scenarios thực hành

### Scenario 1: Normal Operations
1. Tạo 3 users: alice, bob, charlie
2. Alice gửi 50 coins cho Bob
3. Bob mine block
4. Bob gửi 20 coins cho Charlie
5. Charlie mine block
6. Verify tất cả balances

### Scenario 2: Sybil Attack
1. Tạo 5 honest nodes
2. Launch Sybil attack (20 fake nodes)
3. Analyze network control ratio
4. Demonstrate consensus manipulation
5. Cleanup attack

### Scenario 3: Eclipse Attack
1. Login một target node
2. Connect với several honest peers
3. Launch Eclipse attack
4. Observe complete isolation
5. Feed false blockchain
6. Restore connections

## 🐛 Troubleshooting

**Q: Port already in use?**  
A: Đóng các instance khác hoặc đợi port được release

**Q: Mining quá lâu?**  
A: Giảm `DIFFICULTY` trong config.py (VD: từ 4 → 3)

**Q: Node không nhận blocks?**  
A: Sync blockchain (Option 13) hoặc reconnect peers (Option 11)

**Q: Balance bị âm?**  
A: Tạo transaction nhiều hơn mining rewards

## 🔮 Future Enhancements

- [ ] Digital signatures (ECDSA)
- [ ] Merkle trees
- [ ] UTXO model
- [ ] Network encryption (TLS)
- [ ] Database storage
- [ ] Web UI dashboard
- [ ] Advanced consensus (PBFT, PoS)
- [ ] Smart contracts support

## 📖 References

- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
- [Ethereum Whitepaper](https://ethereum.org/en/whitepaper/)
- [Sybil Attack Paper](https://www.microsoft.com/en-us/research/publication/the-sybil-attack/)
- [Eclipse Attacks on Bitcoin's Peer-to-Peer Network](https://eprint.iacr.org/2015/263.pdf)

## 📝 License

MIT License - Free to use for educational purposes

## 👨‍💻 Author

Created for blockchain security education and research

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## ⭐ Ghi chú quan trọng

### Tính năng đã implement:
✅ Genesis block tự động cho mỗi node  
✅ File-based account storage (không mã hóa - như yêu cầu)  
✅ Block structure: previous_hash, hash, transaction, timestamp  
✅ 1 transaction per block  
✅ Node tự động join network sau register  
✅ Random connection đến tối đa 8 peers  
✅ P2P transactions  
✅ Mining với POW  
✅ Broadcasting transactions và blocks  

### Tính năng bổ sung:
✅ Network Manager để quản lý tất cả nodes  
✅ Peer Discovery tự động  
✅ Chain Synchronization  
✅ Consensus mechanism (longest chain)  
✅ Transaction pool  
✅ Mining rewards  
✅ Balance tracking  
✅ Chain validation  
✅ Complete Sybil Attack simulator  
✅ Complete Eclipse Attack simulator  

Enjoy learning blockchain security! 🔐🔗
