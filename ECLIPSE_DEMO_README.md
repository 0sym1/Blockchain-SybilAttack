# Eclipse Attack Demo - Standalone Script

## 📖 Overview

This is a **standalone demonstration** of Eclipse Attack with Double-Spending on the blockchain network. It runs independently from the main system and provides a realistic simulation of how Eclipse attacks work in P2P networks.

## 🎯 Features

### ✅ What This Demo Does

1. **Creates Malicious Accounts**
   - Registers real accounts in the system
   - Each malicious node has full blockchain capabilities
   - Customizable number of attackers

2. **Starts Malicious Network**
   - Launches malicious nodes as real P2P nodes
   - Connects them into coordinated network
   - Each node has unique port and identity

3. **Target Selection**
   - Lists all legitimate nodes in network
   - Interactive selection of victim node
   - Shows node details (username, ID, URL)

4. **Eclipse Attack Execution**
   - Isolates target node from legitimate network
   - Surrounds target with malicious nodes
   - Controls target's view of blockchain

5. **Double-Spending Demonstration**
   - Creates two conflicting transactions
   - Main network sees Transaction 1
   - Target sees Transaction 2 (double-spend)
   - Shows how victim is deceived

6. **Complete Cleanup**
   - Stops all malicious nodes
   - Deletes malicious accounts
   - Removes all traces of attack

## 🚀 Usage

### Prerequisites

1. **Main system must be running**
   - Have some legitimate nodes in network
   - At least 1 active user account

2. **Run the demo**:
```bash
python demo_eclipse_attack.py
```

### Demo Flow

```
┌─────────────────────────────────────────┐
│  STEP 1: Create Malicious Accounts      │
│  - Input: Number of attackers           │
│  - Creates: Real user accounts          │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  STEP 2: Start Malicious Nodes          │
│  - Starts: Flask servers for each       │
│  - Registers: Nodes in network          │
│  - Connects: Malicious nodes together   │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  STEP 3: Select Target                  │
│  - Shows: All legitimate nodes          │
│  - Input: Choose victim                 │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  STEP 4: Eclipse Attack                 │
│  - Isolates: Target from network        │
│  - Surrounds: Target with malicious     │
│  - Controls: Target's blockchain view   │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  STEP 5: Double-Spending Attack         │
│  - TX1: Send 50 coins to Target (real)  │
│  - TX2: Send 50 coins to Attacker (fake)│
│  - Mines: TX1 on main network           │
│  - Shows: Target sees TX2 only          │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  STEP 6: Cleanup                        │
│  - Stops: All malicious nodes           │
│  - Deletes: All malicious accounts      │
│  - Clears: Network of attack traces     │
└─────────────────────────────────────────┘
```

## 📋 Example Session

```bash
$ python demo_eclipse_attack.py

🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑
ECLIPSE ATTACK DEMONSTRATION
Simulating Real-World Eclipse Attack with Double-Spending
🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑

📊 Current network status:
================================================================================
NETWORK NODES
================================================================================
#     Username             Node ID                                  URL                      
--------------------------------------------------------------------------------
1     alice                f4a8b2c6...                              http://127.0.0.1:5000    
2     bob                  9c3d1e5f...                              http://127.0.0.1:5001    
3     charlie              2a7f9b4e...                              http://127.0.0.1:5002    
================================================================================

Press Enter to start demo...

================================================================================
STEP 1: CREATE MALICIOUS ACCOUNTS
================================================================================

💀 Enter number of malicious nodes to create (default 8): 5

🔨 Creating 5 malicious accounts...
  ✓ Created: Malicious_001
  ✓ Created: Malicious_002
  ✓ Created: Malicious_003
  ✓ Created: Malicious_004
  ✓ Created: Malicious_005

✅ Created 5 malicious accounts

================================================================================
STEP 2: START MALICIOUS NODES
================================================================================

🚀 Starting 5 malicious nodes...
  ✓ Started: Malicious_001 @ http://127.0.0.1:5003
  ✓ Started: Malicious_002 @ http://127.0.0.1:5004
  ✓ Started: Malicious_003 @ http://127.0.0.1:5005
  ✓ Started: Malicious_004 @ http://127.0.0.1:5006
  ✓ Started: Malicious_005 @ http://127.0.0.1:5007

✅ Started 5 malicious nodes

🔗 Connecting malicious nodes to each other...
✅ Malicious network established

================================================================================
STEP 3: SELECT TARGET NODE
================================================================================

📋 Available legitimate nodes:
#     Username             Node ID             URL                      
----------------------------------------------------------------------
1     alice                f4a8b2c6...         http://127.0.0.1:5000    
2     bob                  9c3d1e5f...         http://127.0.0.1:5001    
3     charlie              2a7f9b4e...         http://127.0.0.1:5002    

🎯 Select target node (1-3): 2

✅ Target selected: bob @ http://127.0.0.1:5001

Press Enter to continue...

================================================================================
STEP 4: ECLIPSE ATTACK - ISOLATE TARGET
================================================================================

🌑 Eclipsing target: bob
   URL: http://127.0.0.1:5001

📊 Target status:
   Chain length: 5
   Current peers: 2
   Pending tx: 0

💾 Saving target's original peers...
   (Peer list saved)

✂️ Disconnecting target from legitimate peers...
   (Simulated: Target's connections to legitimate nodes severed)

🔗 Surrounding target with malicious nodes...
   ✓ Connected: Malicious_001
   ✓ Connected: Malicious_002
   ✓ Connected: Malicious_003
   ✓ Connected: Malicious_004
   ✓ Connected: Malicious_005

✅ Target eclipsed! Surrounded by 5 malicious nodes
   Target is now isolated in malicious network

Press Enter to demonstrate double-spending...

================================================================================
STEP 5: DOUBLE-SPENDING ATTACK
================================================================================

💰 Demonstrating double-spending attack...
   Attacker: Malicious_001
   Target (Victim): bob

📊 Attacker balance: 100 coins

📤 Transaction 1: Malicious_001 → bob (50 coins)
   Creating legitimate transaction on main chain...
   ✓ Transaction 1 created
   📡 Broadcasting to malicious network...

📤 Transaction 2: Malicious_001 → Malicious_002 (50 coins)
   ⚠️ DOUBLE-SPENDING the same 50 coins!
   Creating alternative transaction on shadow chain...
   ✓ Transaction 2 sent to target
   🎭 Target sees different transaction than main network!

⛏️ Mining Transaction 1 on malicious network...
   ✓ Block mined on main chain
   📡 Broadcasting to malicious network...

================================================================================
ATTACK RESULT
================================================================================

🌐 Main Network (Malicious nodes):
   Chain: Malicious_001 sent 50 coins to bob
   Status: Mined and confirmed

🌑 Shadow Network (Target node):
   Pending: Malicious_001 sent 50 coins to Malicious_002
   Status: NOT mined (isolated)

⚠️ DOUBLE-SPENDING SUCCESSFUL!
   - Main network thinks target received 50 coins
   - Target thinks coins went to Malicious_002
   - Target is isolated and sees different blockchain!
   - Once goods delivered, attacker can reveal real chain

================================================================================
STEP 6: CLEANUP
================================================================================

⚠️ Remove all malicious nodes and accounts? (yes/no): yes

🧹 Cleaning up...

🛑 Stopping malicious nodes...
   ✓ Stopped: Malicious_001
   ✓ Stopped: Malicious_002
   ✓ Stopped: Malicious_003
   ✓ Stopped: Malicious_004
   ✓ Stopped: Malicious_005

🗑️ Deleting malicious accounts...
   ✓ Deleted: Malicious_001
   ✓ Deleted: Malicious_002
   ✓ Deleted: Malicious_003
   ✓ Deleted: Malicious_004
   ✓ Deleted: Malicious_005

✅ Cleanup complete!
   Removed 5 nodes
   Deleted 5 accounts

================================================================================
DEMO COMPLETE
================================================================================

💡 Key Takeaways:
   1. Eclipse attack isolates victim node
   2. Attacker controls victim's view of blockchain
   3. Enables double-spending attack
   4. Victim accepts fake transaction
   5. Real network has different blockchain

✅ Demo finished successfully!
```

## 🎓 Educational Value

### What Students Learn

1. **P2P Network Vulnerabilities**
   - How node isolation works
   - Importance of peer diversity
   - Network topology matters

2. **Eclipse Attack Mechanics**
   - Attacker surrounds victim
   - Controls information flow
   - Creates alternative reality

3. **Double-Spending Exploit**
   - Same coins spent twice
   - Different chains for different nodes
   - Consensus manipulation

4. **Defense Strategies**
   - Need for diverse peer connections
   - Importance of chain validation
   - Network monitoring

## ⚙️ Technical Details

### Architecture

```
┌─────────────┐
│ Main System │ ← Legitimate users running normally
└─────────────┘

┌──────────────────┐
│ Demo Script      │ ← Runs independently
│ - Creates nodes  │
│ - Manages attack │
│ - Cleans up      │
└──────────────────┘

Network Registry (network_nodes.txt)
├── Legitimate nodes
└── Malicious nodes (during attack)

Account Storage (accounts/*.txt)
├── Legitimate accounts
└── Malicious accounts (during attack)
```

### Node Capabilities

Each malicious node has:
- ✅ Full blockchain
- ✅ POW mining
- ✅ Transaction creation
- ✅ Peer connections
- ✅ Flask API server
- ✅ Network registration

### Attack Flow

```
Normal Network:              Eclipse Network:
┌─────┐                     ┌─────┐
│  A  │─────┐               │  A  │  (isolated)
└─────┘     │               └─────┘
            ↓                   ↓
┌─────┐   ┌─────┐          ┌─────┐
│  B  │───│  C  │          │ MA1 │───┐
└─────┘   └─────┘          └─────┘   │
            ↑                   ↓     ↓
┌─────┐    │               ┌─────┐ ┌─────┐
│  D  │────┘               │ MA2 │─│ MA3 │
└─────┘                    └─────┘ └─────┘

Legitimate peers          Malicious attackers
```

## 🔒 Security Implications

### Real-World Risks

1. **Cryptocurrency Exchanges**
   - Accept deposits based on fake chain
   - Attacker withdraws before revealing real chain

2. **Payment Systems**
   - Merchant accepts payment
   - Payment doesn't exist on real blockchain

3. **Smart Contracts**
   - Contract executes based on fake state
   - Real state is different

### Mitigations

1. **Multiple Independent Peers**
   - Connect to diverse nodes
   - Verify across multiple sources

2. **Confirmation Delays**
   - Wait for multiple confirmations
   - Check with multiple nodes

3. **Network Monitoring**
   - Detect unusual peer patterns
   - Alert on isolation attempts

## 📚 Related Concepts

- **Sybil Attack**: Creating many fake identities
- **51% Attack**: Controlling majority of mining power
- **Selfish Mining**: Withholding blocks for advantage
- **Network Partition**: Splitting network into segments

## 🛠️ Customization

### Modify Attack Parameters

Edit script variables:
```python
# Number of malicious nodes (default 8)
count = int(input("Enter number: "))

# Transaction amount for double-spend
amount = 50  # Change this value

# MAX_PEERS limit from config.py
config.MAX_PEERS = 8
```

### Add Features

- Transaction history manipulation
- Chain reorganization attacks
- Timestamp manipulation
- Difficulty adjustment attacks

## ⚠️ Disclaimer

**Educational Purpose Only**

This demonstration is for:
- ✅ Learning blockchain security
- ✅ Understanding P2P vulnerabilities
- ✅ Research and education

**DO NOT USE FOR:**
- ❌ Attacking real networks
- ❌ Stealing cryptocurrency
- ❌ Malicious purposes

## 📞 Support

For questions or issues:
- Check main system documentation
- Review blockchain security papers
- Study P2P network protocols

---

**Last Updated**: 2025-10-24  
**Version**: 1.0  
**Author**: Blockchain Security Demo Team
