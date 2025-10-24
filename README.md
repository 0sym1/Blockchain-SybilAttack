# Blockchain Sybil & Eclipse Attack Demo

Hệ thống blockchain demo để minh họa Sybil Attack và Eclipse Attack.

## Tính năng

### Core Features
- ✅ Hệ thống blockchain cơ bản với Genesis Block
- ✅ Đăng ký/Đăng nhập người dùng (lưu trữ file txt)
- ✅ **Initial Balance: 100 coins** cho mỗi user mới
- ✅ Proof of Work mining với độ khó có thể điều chỉnh
- ✅ Mining rewards: 10 coins/block
- ✅ Peer-to-peer network (mỗi node kết nối tối đa 8 peers)
- ✅ Transaction pool và broadcasting
- ✅ Chain synchronization giữa các nodes
- ✅ Dynamic balance calculation từ blockchain history

### Attack Simulation
- ⚔️ Sybil Attack: Tạo nhiều node giả mạo
- ⚔️ Eclipse Attack: Cô lập một node bằng cách kiểm soát tất cả kết nối của nó

## Cấu trúc Project

```
Blockchain-SybilAttack/
├── core/
│   ├── __init__.py
│   ├── block.py              # Block class
│   ├── blockchain.py         # Blockchain class
│   ├── transaction.py        # Transaction class
│   └── proof_of_work.py      # Mining mechanism
├── network/
│   ├── __init__.py
│   ├── node.py               # Node class với P2P networking
│   ├── network_manager.py    # Quản lý danh sách nodes
│   └── peer_discovery.py     # Tìm kiếm và kết nối peers
├── auth/
│   ├── __init__.py
│   └── user_manager.py       # Đăng ký/đăng nhập
├── attack/
│   ├── __init__.py
│   ├── sybil_attack.py       # Simulator Sybil attack
│   └── eclipse_attack.py     # Simulator Eclipse attack
├── accounts/                  # Folder lưu tài khoản (auto-generated)
├── main.py                    # Entry point
├── config.py                  # Configuration
└── requirements.txt
```

## Cài đặt

```bash
pip install -r requirements.txt
```

## Sử dụng

### 1. Khởi động hệ thống
```bash
python main.py
```

### 2. Menu chính
- Đăng ký tài khoản mới
- Đăng nhập
- Tạo giao dịch
- Mine block
- Xem blockchain
- Kết nối với peers
- Simulate Sybil Attack
- Simulate Eclipse Attack

## Chi tiết kỹ thuật

### Block Structure
```
{
    "index": int,
    "timestamp": float,
    "transaction": Transaction,
    "previous_hash": str,
    "hash": str,
    "nonce": int
}
```

### Node Connection
- Mỗi node kết nối tối đa 8 peers ngẫu nhiên
- Sử dụng Flask API để giao tiếp giữa các nodes
- Tự động đồng bộ blockchain khi kết nối

### Mining
- Proof of Work với độ khó có thể điều chỉnh
- Target: hash bắt đầu với số lượng số 0 nhất định

## Cảnh báo

⚠️ Đây là project demo cho mục đích học tập. KHÔNG sử dụng trong môi trường production.
