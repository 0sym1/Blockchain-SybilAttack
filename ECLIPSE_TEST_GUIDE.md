# Quick Test Guide - Eclipse Attack Demo

## 🚀 Quick Start

### Step 1: Prepare System
```bash
# Terminal 1: Start main system
python main.py

# Create 2-3 legitimate accounts
# Register: alice, bob, charlie
# Login each account (in separate terminals if needed)
```

### Step 2: Run Eclipse Demo
```bash
# Terminal 2: Run demo script
python demo_eclipse_attack.py
```

### Step 3: Follow Demo Prompts

**Prompt 1**: Number of malicious nodes
```
💀 Enter number of malicious nodes to create (default 8): 5
```
→ Enter `5` or press Enter for default

**Prompt 2**: Select target
```
🎯 Select target node (1-3): 2
```
→ Choose node to attack (e.g., `2` for bob)

**Prompt 3**: Cleanup
```
⚠️ Remove all malicious nodes and accounts? (yes/no): yes
```
→ Enter `yes` to cleanup

## ✅ Expected Output

### Success Indicators
- ✓ 5 malicious accounts created
- ✓ 5 malicious nodes started
- ✓ Target eclipsed (surrounded by malicious nodes)
- ✓ Double-spending demonstrated
- ✓ Cleanup completed

### Demo Flow
```
Create Accounts (10s)
      ↓
Start Nodes (5s)
      ↓
Select Target (User input)
      ↓
Eclipse Attack (5s)
      ↓
Double-Spending (5s)
      ↓
Cleanup (5s)
      ↓
DONE (~40s total)
```

## 🧪 Test Scenarios

### Scenario 1: Basic Demo (Recommended)
```
Malicious nodes: 5
Target: Any legitimate node
Result: Clean double-spending demonstration
```

### Scenario 2: Maximum Attack
```
Malicious nodes: 8 (MAX_PEERS)
Target: Richest node
Result: Complete isolation
```

### Scenario 3: Minimal Attack
```
Malicious nodes: 3
Target: Any node
Result: Partial eclipse (easier to escape)
```

## 📊 Verification

### Check Network Status
```bash
# In main system
# Choose option: 12. View network status

# Before attack:
- alice (5000)
- bob (5001)
- charlie (5002)

# During attack:
- alice (5000)
- bob (5001) ← Target
- charlie (5002)
- Malicious_001 (5003)
- Malicious_002 (5004)
- Malicious_003 (5005)
- Malicious_004 (5006)
- Malicious_005 (5007)

# After cleanup:
- alice (5000)
- bob (5001)
- charlie (5002)
```

### Check Accounts
```bash
# In main system
# Choose option: 4. List all accounts

# Before attack:
- alice
- bob
- charlie

# During attack:
- alice
- bob
- charlie
- Malicious_001
- Malicious_002
- Malicious_003
- Malicious_004
- Malicious_005

# After cleanup:
- alice
- bob
- charlie
```

## 🐛 Troubleshooting

### Issue 1: "No nodes in network"
**Solution**: Create and login legitimate accounts first
```bash
python main.py
1. Register new account
2. Login
```

### Issue 2: Port conflicts
**Solution**: Check if ports 5000-5020 are free
```bash
# Windows
netstat -ano | findstr "500"

# Kill process if needed
taskkill /F /PID <pid>
```

### Issue 3: Transaction validation fails
**Solution**: This is expected! Demo shows the attack anyway
```
⚠️ Attacker has insufficient funds for demo!
   Creating test transaction anyway...
```

### Issue 4: Cleanup fails
**Solution**: Manually delete files
```bash
# Delete malicious account files
rm accounts/Malicious_*.txt

# Or in Windows
del accounts\Malicious_*.txt
```

## 💡 Tips

### For Best Results
1. Have 2-3 legitimate nodes running
2. Use default 5-8 malicious nodes
3. Select a node that has transactions
4. Always run cleanup at the end

### For Teaching
1. Show network before attack
2. Explain each step during demo
3. Point out key moments:
   - Isolation
   - Double-spending
   - Different chains
4. Show network after cleanup

### For Development
1. Check console output carefully
2. Monitor Flask server logs
3. Inspect network_nodes.txt
4. Review blockchain states

## 🎓 Demo Script

**For Instructor**:

```
[Show slide: P2P Network Architecture]
"Let's see how Eclipse Attack works in practice."

[Run demo_eclipse_attack.py]
"I'm creating 5 malicious nodes..."
[Wait for accounts creation]

[Show network status in main system]
"Notice we now have 5 new nodes in the network."

[Continue demo]
"I'll select Bob as our target victim."
"Watch as we surround Bob with malicious nodes..."

[Point at screen during isolation]
"Bob is now isolated. He can only talk to our nodes."

[During double-spending]
"Now we're sending the same 50 coins twice!"
"The main network sees one transaction..."
"But Bob sees a different transaction!"

[Show result]
"This is the power of Eclipse Attack."
"Bob is completely deceived about what's happening."

[Run cleanup]
"Let's clean up our attack..."
"All malicious nodes removed!"

[Show final network]
"Back to normal. No traces left."
```

## 📸 Screenshots

### Before Attack
```
NETWORK NODES
alice     @ 5000
bob       @ 5001  ← Normal network
charlie   @ 5002
```

### During Attack
```
NETWORK NODES
alice            @ 5000
bob              @ 5001  ← Eclipsed!
charlie          @ 5002
Malicious_001    @ 5003  ╮
Malicious_002    @ 5004  │
Malicious_003    @ 5005  ├─ Attackers
Malicious_004    @ 5006  │
Malicious_005    @ 5007  ╯
```

### After Cleanup
```
NETWORK NODES
alice     @ 5000
bob       @ 5001  ← Restored
charlie   @ 5002
```

## ⏱️ Time Estimates

| Step | Time | Notes |
|------|------|-------|
| Prepare system | 2 min | Create accounts |
| Run demo | 1 min | Automatic |
| Explanation | 5 min | If teaching |
| Cleanup | 10 sec | Automatic |
| **Total** | **3-8 min** | Depends on teaching |

## ✅ Checklist

- [ ] Main system running
- [ ] 2+ legitimate accounts created
- [ ] Accounts logged in
- [ ] Run demo script
- [ ] Enter number of attackers
- [ ] Select target
- [ ] Watch demonstration
- [ ] Run cleanup
- [ ] Verify network restored

---

**Ready to try?** Run: `python demo_eclipse_attack.py`
