# Dead Peers Cleanup - Fix Documentation

## 🐛 Vấn Đề

**Hiện tượng:**
Sau khi tắt malicious nodes trong Eclipse attack demo, target node vẫn hiển thị `8/8 peers` dù các peers đó đã offline.

**Nguyên nhân:**
- Node lưu danh sách peers trong memory (`self.peers`)
- Khi peer offline, node KHÔNG tự động phát hiện
- Peers chết vẫn nằm trong danh sách → chiếm slot connection
- MAX_PEERS limit bị block bởi dead peers

## ✅ Giải Pháp

### 1. **Health Check Mechanism**

Thêm method kiểm tra peer còn sống:

```python
# network/node.py
def check_peer_health(self, peer_url, timeout=2):
    """Kiểm tra peer còn hoạt động không"""
    try:
        response = requests.get(f"{peer_url}/info", timeout=timeout)
        return response.status_code == 200
    except:
        return False  # Peer chết hoặc unreachable
```

### 2. **Auto Cleanup Stale Peers**

Thêm method tự động xóa peers chết:

```python
def cleanup_stale_peers(self):
    """Xóa tất cả peers không còn hoạt động"""
    stale_peers = []
    
    # Kiểm tra từng peer
    for peer_id, peer_url in list(self.peers.items()):
        if not self.check_peer_health(peer_url, timeout=1):
            stale_peers.append(peer_id)
    
    # Xóa các stale peers
    for peer_id in stale_peers:
        print(f"⚠️ Removing stale peer: {peer_id[:8]}...")
        self.remove_peer(peer_id)
    
    return len(stale_peers)
```

### 3. **API Endpoint**

Thêm endpoint để trigger cleanup:

```python
@app.route('/cleanup_peers', methods=['POST'])
def cleanup_peers():
    """Xóa tất cả peers không còn hoạt động"""
    removed = self.cleanup_stale_peers()
    return jsonify({
        'message': f'Cleaned up {removed} stale peer(s)',
        'removed_count': removed,
        'remaining_peers': len(self.peers)
    })
```

### 4. **Auto Cleanup on Broadcast**

Cleanup tự động khi broadcast fail:

```python
def broadcast_transaction(self, transaction):
    """Broadcast với auto cleanup"""
    failed_peers = []
    
    for peer_id, peer_url in list(self.peers.items()):
        try:
            response = requests.post(...)
            if response.status_code != 200:
                failed_peers.append(peer_id)
        except:
            failed_peers.append(peer_id)
    
    # Auto remove failed peers
    if failed_peers:
        for peer_id in failed_peers:
            self.remove_peer(peer_id)
```

### 5. **Auto Cleanup on /info**

Cleanup mỗi khi check node info:

```python
@app.route('/info')
def info():
    # Auto cleanup before returning info
    self.cleanup_stale_peers()
    
    return jsonify({
        'peers_count': len(self.peers),  # Accurate count!
        ...
    })
```

## 🎯 Cách Sử Dụng

### **Option 1: Manual Cleanup (Menu)**

```bash
python main.py
# Login vào target node
# Chọn option 14: "Cleanup dead peers"
```

**Output:**
```
🧹 Cleaning up dead peers...
Current peers: 8/8

⚠️ Removing stale peer: abc12345... (unreachable)
⚠️ Removing stale peer: def67890... (unreachable)
...

✅ Removed 8 dead peer(s)
💡 You now have 0/8 active peers
   8 slot(s) available for new connections
```

### **Option 2: API Call**

```bash
curl -X POST http://localhost:5000/cleanup_peers
```

**Response:**
```json
{
  "message": "Cleaned up 8 stale peer(s)",
  "removed_count": 8,
  "remaining_peers": 0
}
```

### **Option 3: Automatic (Eclipse Demo)**

Demo tự động cleanup sau khi shutdown malicious nodes:

```python
# demo_eclipse_attack.py - Phase 3
# Shutdown malicious nodes
shutdown_malicious_nodes()

# Auto cleanup on target
requests.post(f"{target_url}/cleanup_peers")

# Sync with legitimate network
requests.post(f"{target_url}/sync")
```

**Flow:**
```
1. Malicious nodes shutdown → All offline
2. Target cleanup_peers → Removes 8/8 dead peers
3. Target sync → Discovers legitimate peers
4. Target reconnects → Accepts legitimate chain
```

## 📊 Before & After

### **Before Fix:**

```
Target Node Status:
  Peers: 8/8 (all dead!)
  - Malicious_001 (offline) ❌
  - Malicious_002 (offline) ❌
  - ...
  - Malicious_008 (offline) ❌

Problem: No slots for legitimate peers!
```

### **After Fix:**

```
Target Node Status:
  Peers: 0/8 (after cleanup)
  
Auto cleanup triggered...
⚠️ Removing 8 stale peers

Target Node Status:
  Peers: 2/8 (legitimate nodes)
  - Alice (online) ✅
  - Bob (online) ✅
  
Available slots: 6/8 ✅
```

## 🔧 Technical Details

### **Health Check Logic:**

```python
# Timeout: 1-2 seconds
# Method: GET /info
# Success: HTTP 200
# Fail: Timeout, Connection Error, HTTP error
```

### **When Cleanup Triggers:**

1. **Manual**: User selects menu option 14
2. **API**: POST /cleanup_peers
3. **Auto on /info**: Mỗi lần check node info
4. **Auto on broadcast**: Khi broadcast transaction/block fail
5. **Eclipse demo**: Sau khi shutdown malicious nodes

### **Performance:**

```
Check 8 peers with 1s timeout:
- Sequential: ~8 seconds (worst case)
- Parallel: Could optimize with threading
```

## ⚠️ Cảnh Báo

1. **Network Partitions**: Cleanup có thể xóa peers tạm thời unreachable
2. **Timeouts**: Timeout quá ngắn → false positives
3. **Concurrent Access**: Cần careful với thread safety

## 🎓 Bài Học

### **Design Principle:**

```
❌ BAD: Assume peers always online
✅ GOOD: Continuously monitor peer health

❌ BAD: Never cleanup dead connections  
✅ GOOD: Auto cleanup + manual trigger

❌ BAD: Block slots forever with dead peers
✅ GOOD: Free slots when peers die
```

### **Real-World Implications:**

- **Bitcoin**: Uses ping/pong messages for peer health
- **Ethereum**: Disconnect after N failed messages
- **P2P Best Practice**: Regular health checks + exponential backoff

## 📚 Related Files

- `network/node.py` - Health check & cleanup logic
- `main.py` - Menu option 14
- `demo_eclipse_attack.py` - Auto cleanup in Phase 3
- `ECLIPSE_ATTACK_GUIDE.md` - Attack documentation

## 🔗 Summary

**Problem:** Dead peers block connection slots
**Solution:** Health check + auto cleanup
**Result:** Dynamic peer management with freed slots

---

**Status:** ✅ Fixed - Dead peers automatically detected and removed
