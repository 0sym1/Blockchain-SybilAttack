# Eclipse Attack - Known Issue & Fix

## 🐛 **Issue: Target Node Shows 8/8 Peers After Attack**

### **Symptoms:**
```
After Eclipse attack finishes:
- Malicious nodes are shutdown (offline)
- Target node still shows: 👥 Peers: 8/8
- All 8 peers are DEAD (unreachable)
- Cannot connect to legitimate nodes
```

### **Root Cause:**
```python
# When peers disconnect/shutdown:
1. Malicious nodes stop Flask servers
2. Peers become unreachable
3. Target node DOESN'T auto-detect
4. Dead peers remain in self.peers dict
5. All 8 slots blocked by dead peers
```

## ✅ **Quick Fix (3 Options)**

### **Option 1: Cleanup Script (Fastest)**
```bash
python cleanup_target_node.py 5000
# Replace 5000 with target port
```

### **Option 2: Menu (In Target Terminal)**
```
Select option 14: Cleanup dead peers
Then option 11: Connect to peers
```

### **Option 3: Restart**
```
Select option 3: Logout
Select option 2: Login
```

## 📊 **Expected Results**

### Before Cleanup:
```
👥 Peers: 8/8
   - Malicious_001 (DEAD) ❌
   - Malicious_002 (DEAD) ❌
   - ... 6 more dead peers
Status: Cannot connect to legitimate nodes
```

### After Cleanup:
```
👥 Peers: 0/8
   (All dead peers removed)
Status: Ready to connect
```

### After Reconnect:
```
👥 Peers: 2/8
   - Alice (ALIVE) ✅
   - Bob (ALIVE) ✅
Status: Normal operation
```

## 🔧 **Why Not Auto Cleanup?**

```
❌ BAD Design (Auto cleanup):
├─ Demo checks /info → triggers cleanup
├─ Cleanup removes malicious peers
├─ Eclipse attack fails!
└─ Cannot demonstrate attack

✅ GOOD Design (Manual cleanup):
├─ Demo checks /info → NO auto cleanup
├─ Malicious peers stay connected
├─ Eclipse attack succeeds!
├─ After demo → user cleans up manually
└─ Can demonstrate attack properly
```

## 🎯 **Complete Recovery Steps**

```
1️⃣ Run Eclipse Demo
   → Target isolated: 8/8 malicious peers

2️⃣ Demo Completes
   → Malicious nodes shutdown
   → Target still shows: 8/8 (all dead)

3️⃣ Cleanup Dead Peers
   Method A: python cleanup_target_node.py 5000
   Method B: Menu option 14
   Method C: Logout/Login
   → Target shows: 0/8 peers

4️⃣ Reconnect to Network
   → Menu option 11: Connect to peers
   → Target shows: 2/8 peers (legitimate)

5️⃣ Verify Recovery
   → Check balance
   → Create transaction
   → Mine block
   → All working normally ✅
```

## 📝 **Key Files**

```
cleanup_target_node.py       # Quick cleanup script
TARGET_NODE_RECOVERY.md      # Detailed guide
network/node.py              # /cleanup_peers API
main.py                      # Option 14: Cleanup dead peers
demo_eclipse_attack.py       # Shows recovery instructions
```

## 💡 **Pro Tip**

Add this to your workflow:

```bash
# After EVERY Eclipse demo:
python cleanup_target_node.py <target_port>

# Or automate in script:
echo "python cleanup_target_node.py 5000" >> cleanup_all.sh
```

---

**Status:** ✅ Known issue with documented workaround
**Impact:** Low (easy fix, doesn't break functionality)
**Priority:** Documentation > Code fix (design choice)
