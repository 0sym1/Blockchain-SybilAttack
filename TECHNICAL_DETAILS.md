# Blockchain Sybil Attack Demo - Giải thích chi tiết

## Tổng quan kiến trúc

### 1. Core Module (core/)
- **block.py**: Định nghĩa cấu trúc Block với các thuộc tính:
  - index: vị trí block trong chain
  - transaction: giao dịch được lưu (1 transaction/block)
  - previous_hash: hash của block trước
  - hash: hash của block hiện tại
  - timestamp: thời gian tạo block
  - nonce: số dùng cho Proof of Work

- **blockchain.py**: Quản lý chuỗi blocks:
  - Genesis block tự động tạo khi khởi tạo
  - Pending transactions pool
  - Mining với Proof of Work
  - Chain validation
  - Consensus (longest chain rule)

- **transaction.py**: Cấu trúc giao dịch P2P:
  - sender: người gửi
  - receiver: người nhận
  - amount: số lượng coin
  - timestamp: thời gian

- **proof_of_work.py**: Thuật toán mining:
  - Tìm nonce sao cho hash bắt đầu với n số 0
  - Độ khó điều chỉnh được (config.DIFFICULTY)

### 2. Network Module (network/)
- **node.py**: Node trong mạng P2P:
  - Flask API server cho giao tiếp
  - Quản lý blockchain local
  - Kết nối với peers (max 8)
  - Broadcasting transactions/blocks
  - Chain synchronization

- **network_manager.py**: Quản lý mạng:
  - Registry tất cả nodes
  - Lưu trữ thông tin nodes (file txt)
  - Random peer selection
  - Node discovery

- **peer_discovery.py**: Tìm kiếm peers:
  - Tự động kết nối random peers
  - Maintain peer connections
  - Reconnection logic

### 3. Auth Module (auth/)
- **user_manager.py**: Quản lý người dùng:
  - Đăng ký/đăng nhập
  - Lưu thông tin trong folder accounts/
  - Mỗi user = 1 file txt
  - Format: username, password, blockchain data

### 4. Attack Module (attack/)
- **sybil_attack.py**: Mô phỏng Sybil Attack:
  - Tạo nhiều node giả mạo
  - Chiếm đoạt quyền kiểm soát mạng
  - Kết nối các Sybil nodes với nhau
  - Phân tích tỷ lệ kiểm soát mạng

- **eclipse_attack.py**: Mô phỏng Eclipse Attack:
  - Cô lập target node
  - Kiểm soát tất cả connections
  - Feed false blockchain data
  - Demo double-spending potential

## Cách hoạt động

### Quy trình đăng ký và tham gia mạng:
1. User đăng ký → tạo file txt trong accounts/
2. Login → tạo Node với blockchain
3. Node start → Flask server chạy trên port tự động
4. Node register vào NetworkManager
5. PeerDiscovery tự động kết nối random 8 peers
6. Node ready để giao dịch và mining

### Quy trình giao dịch:
1. User tạo transaction (sender → receiver)
2. Transaction thêm vào pending pool
3. Transaction broadcast đến tất cả peers
4. Peers nhận và thêm vào pending pool của họ
5. Miner mine block với 1 transaction
6. Block broadcast đến network
7. Peers validate và thêm block vào chain

### Quy trình Sybil Attack:
1. Attacker tạo nhiều Sybil nodes (20+ nodes)
2. Sybil nodes join network
3. Sybil nodes kết nối với nhau
4. Chiếm >50% mạng
5. Có thể manipulate consensus
6. Có thể isolate honest nodes

### Quy trình Eclipse Attack:
1. Attacker tạo 8 malicious nodes
2. Target node disconnect khỏi honest peers
3. Malicious nodes kết nối với target
4. Target bị cô lập hoàn toàn
5. Feed false blockchain cho target
6. Target tin vào fake data

## API Endpoints

Mỗi Node expose các endpoints:
- GET /ping - Health check
- GET /info - Node information
- GET /chain - Lấy blockchain
- POST /add_peer - Thêm peer
- POST /remove_peer - Xóa peer
- POST /transaction/new - Nhận transaction
- POST /block/new - Nhận block
- GET /chain/resolve - Sync blockchain

## Configuration (config.py)

```python
DIFFICULTY = 4              # Độ khó mining (4 số 0)
MINING_REWARD = 10.0        # Phần thưởng mining
BASE_PORT = 5000            # Port bắt đầu
MAX_PEERS = 8               # Số peers tối đa
SYBIL_NODES_COUNT = 20      # Số Sybil nodes
ECLIPSE_MALICIOUS_NODES = 8 # Số nodes để eclipse
```

## Lưu ý quan trọng

1. **Không dùng production**: Project này chỉ demo tấn công
2. **Performance**: Nhiều nodes sẽ tốn tài nguyên
3. **Security**: Không có mã hóa, chỉ plaintext
4. **Consensus**: Sử dụng longest chain rule đơn giản
5. **Mining**: POW đơn giản, không tối ưu

## Mở rộng tương lai

1. Thêm digital signatures (ECDSA)
2. Merkle trees cho transactions
3. UTXO model thay vì balance-based
4. Network encryption (TLS)
5. Persistent storage (database)
6. Web UI dashboard
7. Advanced consensus (PBFT, PoS)
8. Smart contracts support

## Tấn công có thể demo

1. **Sybil Attack**: 
   - Tạo 20+ fake nodes
   - Chiếm >50% mạng
   - Manipulate consensus

2. **Eclipse Attack**:
   - Isolate 1 target node
   - Control tất cả connections
   - Feed fake blockchain

3. **51% Attack**: 
   - Kết hợp Sybil + mining power
   - Double spending
   - Chain reversal

4. **Network Partition**:
   - Split network thành 2 phần
   - Create competing chains
   - Fork demonstration

## Học tập từ project

- Hiểu blockchain cơ bản
- P2P networking
- Proof of Work
- Consensus mechanisms
- Security vulnerabilities
- Attack vectors và countermeasures
