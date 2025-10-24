# Node Duplication Fix - Technical Documentation

## Vấn đề (Issue)

User báo cáo khi chỉ login 1 account duy nhất, nhưng network status hiển thị 2 nodes:
- Cùng username: `a`
- Cùng port: `5000`  
- Khác node_id: `f5844862...` và `aed2c051...`

## Nguyên nhân (Root Cause)

### 1. Flask Server Không Dừng Khi Logout
- Khi user logout, code chỉ unregister node khỏi network registry
- Flask server vẫn chạy trong daemon thread và giữ port
- Port không được giải phóng

### 2. Thiếu Cleanup Khi Login Lại
- Khi user login lại, không có code cleanup old nodes
- Network registry tích lũy stale entries (nodes đã logout nhưng chưa xóa record)
- Dẫn đến duplicate entries cho cùng 1 username

### 3. Không Kiểm Tra Port Conflict
- `find_available_port()` có thể tìm thấy port đã bị chiếm bởi Flask server cũ
- Không có validation để đảm bảo port thực sự free

## Giải pháp (Solution)

### 1. Thêm Stop Server Method (node.py)

**File: `network/node.py`**

```python
def stop(self):
    """Stop node server"""
    try:
        # Gửi request shutdown đến Flask server
        import requests
        requests.post(f"{self.get_url()}/shutdown", timeout=1)
    except:
        pass  # Server có thể đã dừng rồi
```

**Thêm shutdown route:**
```python
@self.app.route('/shutdown', methods=['POST'])
def shutdown():
    """Shutdown Flask server"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()
    return jsonify({'message': 'Server shutting down...'})
```

### 2. Call Stop Method Khi Logout (main.py)

**File: `main.py` - method `logout()`**

```python
def logout(self):
    # ... code khác ...
    
    if self.current_node:
        # ... lưu blockchain ...
        
        # Unregister từ network
        self.network_manager.unregister_node(self.current_node.node_id)
        
        # Stop Flask server ✅ NEW
        print("🛑 Stopping node server...")
        self.current_node.stop()
```

### 3. Cleanup Old Nodes Khi Login (main.py)

**File: `main.py` - method `login()`**

```python
def login(self):
    # ... sau khi login thành công ...
    
    # Cleanup old nodes của username này nếu có ✅ NEW
    print(f"\n🧹 Checking for old nodes...")
    old_nodes = [
        node for node in self.network_manager.get_all_nodes() 
        if node['username'] == username
    ]
    
    if old_nodes:
        print(f"⚠️ Found {len(old_nodes)} old node(s), cleaning up...")
        for old_node in old_nodes:
            # Kill process trên port cũ
            old_port = old_node.get('port')
            if old_port:
                kill_process_on_port(old_port)
            
            # Unregister node
            self.network_manager.unregister_node(old_node['node_id'])
```

### 4. Force Kill Process On Port (main.py)

**File: `main.py` - helper function**

```python
def kill_process_on_port(port):
    """
    Kill process đang chạy trên port (Windows & Linux compatible)
    """
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(
                ['netstat', '-ano'], 
                capture_output=True, 
                text=True,
                timeout=5
            )
            for line in result.stdout.split('\n'):
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    pid = parts[-1]
                    subprocess.run(['taskkill', '/F', '/PID', pid], 
                                   capture_output=True, timeout=5)
                    break
        else:  # Linux/Mac
            result = subprocess.run(
                ['lsof', '-ti', f':{port}'], 
                capture_output=True, 
                text=True,
                timeout=5
            )
            if result.stdout:
                pid = result.stdout.strip()
                subprocess.run(['kill', '-9', pid], timeout=5)
    except:
        pass  # Bỏ qua lỗi
```

### 5. Prevent Duplicate Registration (network_manager.py)

**File: `network/network_manager.py` - method `register_node()`**

```python
def register_node(self, node_id, host, port, username):
    # Check and remove nodes with duplicate username or port ✅ NEW
    nodes_to_remove = []
    for existing_id, existing_node in self.nodes.items():
        if existing_node['username'] == username and existing_id != node_id:
            nodes_to_remove.append(existing_id)
        elif existing_node['port'] == port and existing_id != node_id:
            nodes_to_remove.append(existing_id)
    
    for old_id in nodes_to_remove:
        self.unregister_node(old_id)
    
    # Register new node
    # ... code tiếp theo ...
```

### 6. Prevent Self-Connection (peer_discovery.py)

**File: `network/peer_discovery.py` - method `connect_to_peer()`**

```python
def connect_to_peer(self, peer_id, peer_url):
    # Skip self-connection
    if peer_id == self.node.node_id:
        return False
    
    # Check not connecting to same URL (port) ✅ NEW
    if peer_url == self.node.get_url():
        print(f"Skipped self connection: {peer_url}")
        return False
    
    # ... code tiếp theo ...
```

## Kiến trúc Fix (Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                         LOGIN FLOW                          │
└─────────────────────────────────────────────────────────────┘

1. User nhập username/password
                ↓
2. ✅ Kiểm tra old nodes (NEW)
   - Tìm nodes cùng username trong registry
   - Kill process trên port cũ (subprocess)
   - Unregister từ network_nodes.txt
                ↓
3. Tạo Node mới
   - find_available_port() → port free
   - Node.__init__(username) → tạo Flask app
                ↓
4. Start Flask server
   - Thread(target=_run_server, daemon=True)
   - app.run(port=port)
                ↓
5. Register vào network
   - ✅ Auto-remove duplicates (NEW)
   - Save to network_nodes.txt


┌─────────────────────────────────────────────────────────────┐
│                        LOGOUT FLOW                          │
└─────────────────────────────────────────────────────────────┘

1. User chọn logout
                ↓
2. Save blockchain → account file
                ↓
3. Unregister từ network
                ↓
4. ✅ Stop Flask server (NEW)
   - POST to /shutdown endpoint
   - werkzeug.server.shutdown()
   - Port được giải phóng
                ↓
5. Clear current_node, current_user


┌─────────────────────────────────────────────────────────────┐
│                    PEER CONNECTION FLOW                     │
└─────────────────────────────────────────────────────────────┘

1. Discover peers từ network registry
                ↓
2. Loop through peers
                ↓
3. ✅ Kiểm tra không phải self (NEW)
   - Check node_id khác
   - ✅ Check URL khác (NEW)
                ↓
4. Connect nếu valid
```

## Test Cases

### Test 1: Single Login
```
1. Run program
2. Login với username "a"
3. Chọn "12. View network status"
4. ✅ Expect: 1 node duy nhất với username "a"
```

### Test 2: Logout → Login Again
```
1. Login với username "a"
2. Logout
3. Login lại với username "a"
4. Chọn "12. View network status"
5. ✅ Expect: 1 node duy nhất (old node đã bị xóa)
```

### Test 3: Port Reuse
```
1. Login user "a" → node trên port 5000
2. Logout (port 5000 free)
3. Login user "b" → có thể dùng port 5000
4. ✅ Expect: Không conflict, old node đã cleanup
```

### Test 4: Abnormal Exit
```
1. Login user "a"
2. Ctrl+C (KeyboardInterrupt)
3. Program calls logout() → stop server
4. ✅ Expect: Port 5000 được giải phóng
```

## Migration Notes

### Files Modified
- ✅ `main.py`: Added kill_process_on_port(), updated login/logout
- ✅ `network/node.py`: Added stop() method, /shutdown route
- ✅ `network/network_manager.py`: Enhanced register_node()
- ✅ `network/peer_discovery.py`: Added URL check in connect_to_peer()

### Dependencies
- ✅ `subprocess`: For killing processes (already in stdlib)
- ✅ `socket`: For port checking (already used)

### Backward Compatibility
- ✅ Old network_nodes.txt files still work
- ✅ Old account files still compatible
- ✅ No breaking changes in API endpoints

## Monitoring & Debug

### Check Current Ports
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

### Check Network Registry
```bash
# View current nodes
cat network_nodes.txt
```

### Debug Logs
Program hiện có các logs:
- `🧹 Checking for old nodes...` - Cleanup phase
- `🔪 Killed process X on port Y` - Port cleanup
- `🛑 Stopping node server...` - Server shutdown
- `✓ Removed old node...` - Registry cleanup

## Future Improvements

1. **Heartbeat System**: Auto-remove stale nodes sau timeout (VD: 5 phút không ping)
2. **Graceful Shutdown**: Signal handler cho SIGTERM, SIGINT
3. **Port Pool Management**: Pre-allocate range of ports, track usage
4. **Database Instead of File**: Replace network_nodes.txt với SQLite
5. **Node Recovery**: Auto-reconnect nếu server crash

## Tổng kết (Summary)

Đã fix node duplication bug bằng 4 layers:

1. **Layer 1 (Login)**: Proactive cleanup old nodes before creating new one
2. **Layer 2 (Logout)**: Stop Flask server to free port
3. **Layer 3 (Registration)**: Auto-detect and remove duplicates
4. **Layer 4 (Connection)**: Skip self-connection by URL

✅ Đảm bảo mỗi username chỉ có 1 node active tại một thời điểm.
