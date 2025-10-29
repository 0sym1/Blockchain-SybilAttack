# Target Node Recovery After Eclipse Attack

## 🐛 Issue

After Eclipse attack demo finishes, target node still shows `8/8 peers` even though all malicious nodes are offline.

**Why this happens:**
- Malicious nodes shutdown but target node keeps them in peer list
- Dead peers block all 8 connection slots
- Target cannot connect to legitimate nodes
- Manual cleanup required

## ✅ Quick Fix

### **Option 1: Automated Cleanup Script**

```bash
# Run this from any terminal
python cleanup_target_node.py 5000

# Replace 5000 with your target node's port
```

**What it does:**
- Connects to target node
- Calls `/cleanup_peers` API
- Removes all dead peers
- Shows available connection slots

### **Option 2: Manual Cleanup (from target node)**

In the target node's terminal:

```
Main Menu
  → Option 14: Cleanup dead peers
  → Option 11: Connect to peers
```

**Step-by-step:**
1. Select `14` → Cleanup dead peers
2. All 8 dead malicious nodes removed
3. Select `11` → Connect to peers
4. Target reconnects to legitimate nodes

### **Option 3: Restart Node**

Quickest but loses current session:

```
Main Menu
  → Option 3: Logout
  → Option 2: Login
```

Logging out and back in resets peer connections.

## 📊 Verification

Check if cleanup worked:

```bash
# In target node terminal, check menu header:
👥 Peers: 0/8  ← Dead peers removed ✅
👥 Peers: 8/8  ← Still has dead peers ❌

# After reconnecting:
👥 Peers: 2/8  ← Connected to 2 legitimate nodes ✅
```

## 🔧 Technical Details

### Why auto cleanup during attack would be bad:

```python
# During Eclipse attack:
1. Malicious nodes connect → Target: 8/8 peers
2. Demo checks /info → Would trigger cleanup
3. Cleanup removes malicious peers → Target: 0/8
4. Attack fails! ❌

# Current design (better):
1. Malicious nodes connect → Target: 8/8 peers
2. Demo checks /info → No auto cleanup
3. Attack proceeds → Target isolated ✅
4. After attack → Manual cleanup available
```

### Cleanup API:

```bash
# POST request to cleanup
curl -X POST http://localhost:5000/cleanup_peers

# Response:
{
  "message": "Cleaned up 8 stale peer(s)",
  "removed_count": 8,
  "remaining_peers": 0
}
```

## 🎯 Troubleshooting

### Issue: Script says "node not running"

```
Solution: Make sure target node is still running
Check: Should see Flask logs in target terminal
```

### Issue: Cleanup removes 0 peers

```
Possible reasons:
1. Peers already cleaned up
2. Malicious nodes still running (check network)
3. Firewall blocking health checks

Solution: Use Option 3 (Logout/Login) to force reset
```

### Issue: After cleanup, still 8/8 peers

```
Possible reasons:
1. Cleanup API not implemented (old version)
2. Health check failed (all returned healthy)

Solution:
1. Update node.py to latest version
2. Force restart: Logout → Login
```

## 📝 Demo Flow with Recovery

```
┌────────────────────────────────────────────────────────┐
│ Eclipse Attack Demo                                     │
├────────────────────────────────────────────────────────┤
│ 1. Create 8 malicious nodes                            │
│ 2. Connect to target → Target: 8/8 malicious peers     │
│ 3. Eclipse attack succeeds                             │
│ 4. Double-spending demonstration                       │
│ 5. Malicious nodes shutdown → All offline              │
│ 6. Demo shows recovery instructions ⬇                  │
└────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ Target Node Still Shows: 8/8 peers (all dead!)         │
├────────────────────────────────────────────────────────┤
│ ⚠️ User must manually cleanup dead peers              │
└────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ RECOVERY STEP 1: Cleanup Dead Peers                    │
├────────────────────────────────────────────────────────┤
│ Method A: Run cleanup script                           │
│   $ python cleanup_target_node.py 5000                 │
│                                                         │
│ Method B: Manual menu option                           │
│   Main Menu → 14 (Cleanup dead peers)                  │
│                                                         │
│ Method C: Restart                                       │
│   Main Menu → 3 (Logout) → 2 (Login)                   │
├────────────────────────────────────────────────────────┤
│ Result: Target: 0/8 peers ✅                            │
└────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ RECOVERY STEP 2: Reconnect to Legitimate Network       │
├────────────────────────────────────────────────────────┤
│ Main Menu → 11 (Connect to peers)                      │
│                                                         │
│ Target discovers and connects to:                      │
│   - Alice (legitimate node)                            │
│   - Bob (legitimate node)                              │
├────────────────────────────────────────────────────────┤
│ Result: Target: 2/8 peers (legitimate) ✅              │
└────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ ✅ RECOVERY COMPLETE                                    │
├────────────────────────────────────────────────────────┤
│ • Dead peers removed                                    │
│ • Connected to legitimate nodes                         │
│ • Blockchain synced with real network                   │
│ • Ready for normal operations                           │
└────────────────────────────────────────────────────────┘
```

## 💡 Prevention (Future Improvement)

To avoid this issue in future:

```python
# Add heartbeat mechanism
def start_heartbeat():
    """Auto cleanup dead peers every 30 seconds"""
    while running:
        time.sleep(30)
        cleanup_stale_peers(verbose=False)

# Add peer health monitoring
def monitor_peers():
    """Track peer failures"""
    if peer_failure_count[peer_id] > 3:
        auto_remove_peer(peer_id)
```

## 📚 Related Files

- `cleanup_target_node.py` - Quick cleanup script
- `network/node.py` - Node with `/cleanup_peers` API
- `main.py` - Menu option 14 (Cleanup dead peers)
- `demo_eclipse_attack.py` - Eclipse attack demo

---

**Summary:** After Eclipse attack, run `python cleanup_target_node.py <port>` to remove dead peers and reconnect to legitimate network.
