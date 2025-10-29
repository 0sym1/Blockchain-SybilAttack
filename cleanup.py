"""
Cleanup Utility - Clear all stuck nodes and processes

This script helps clean up:
1. Processes running on blockchain ports (5000-5100)
2. Stale entries in network registry
3. Orphaned account files (optional)

Usage:
    python cleanup.py [options]

Options:
    --ports     Clear processes on ports only
    --registry  Clear network registry only
    --accounts  Clear all accounts (WARNING: deletes all user data!)
    --all       Full cleanup (ports + registry)
"""

import os
import sys
import subprocess
import json


def kill_processes_on_ports(start_port=5000, end_port=5100):
    """
    Kill all processes running on blockchain ports
    
    Args:
        start_port (int): Start of port range
        end_port (int): End of port range
    """
    print("\n" + "="*80)
    print("KILLING PROCESSES ON PORTS")
    print("="*80)
    print(f"Scanning ports {start_port}-{end_port}...")
    
    killed_count = 0
    
    for port in range(start_port, end_port + 1):
        try:
            if os.name == 'nt':  # Windows
                # Find process using port
                result = subprocess.run(
                    ['netstat', '-ano'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                for line in result.stdout.split('\n'):
                    if f':{port}' in line and 'LISTENING' in line:
                        parts = line.split()
                        if len(parts) >= 5:
                            pid = parts[-1]
                            
                            # Get process name
                            try:
                                name_result = subprocess.run(
                                    ['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV', '/NH'],
                                    capture_output=True,
                                    text=True,
                                    timeout=2
                                )
                                process_name = name_result.stdout.split(',')[0].strip('"') if name_result.stdout else 'Unknown'
                            except:
                                process_name = 'Unknown'
                            
                            # Kill process
                            kill_result = subprocess.run(
                                ['taskkill', '/F', '/PID', pid],
                                capture_output=True,
                                timeout=5
                            )
                            
                            if kill_result.returncode == 0:
                                print(f"  ✓ Killed PID {pid} ({process_name}) on port {port}")
                                killed_count += 1
                            else:
                                print(f"  ✗ Failed to kill PID {pid} on port {port}")
            
            else:  # Linux/Mac
                # Find and kill process
                result = subprocess.run(
                    ['lsof', '-ti', f':{port}'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.stdout:
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        if pid:
                            subprocess.run(['kill', '-9', pid], timeout=5)
                            print(f"  ✓ Killed PID {pid} on port {port}")
                            killed_count += 1
        
        except subprocess.TimeoutExpired:
            print(f"  ⚠️ Timeout while checking port {port}")
        except Exception as e:
            # Silently skip ports without processes
            pass
    
    print(f"\n✅ Killed {killed_count} process(es)")
    return killed_count


def clear_network_registry():
    """Clear all entries from network registry"""
    print("\n" + "="*80)
    print("CLEARING NETWORK REGISTRY")
    print("="*80)
    
    registry_file = 'network_nodes.txt'
    
    if not os.path.exists(registry_file):
        print(f"  ℹ️ Registry file not found: {registry_file}")
        return 0
    
    try:
        # Read current registry
        with open(registry_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content:
            print("  ℹ️ Registry already empty")
            return 0
        
        # Parse JSON
        try:
            nodes = json.loads(content)
            node_count = len(nodes)
        except json.JSONDecodeError:
            print("  ⚠️ Registry file corrupted, will clear anyway")
            node_count = "unknown"
        
        # Clear registry
        with open(registry_file, 'w', encoding='utf-8') as f:
            f.write('{}')
        
        print(f"  ✓ Cleared {node_count} node(s) from registry")
        return node_count if isinstance(node_count, int) else 0
        
    except Exception as e:
        print(f"  ✗ Error clearing registry: {str(e)}")
        return 0


def clear_accounts(pattern=None):
    """
    Clear account files
    
    Args:
        pattern (str): Only delete accounts matching pattern (e.g., "Malicious_*")
                       If None, asks for confirmation to delete ALL
    """
    print("\n" + "="*80)
    print("CLEARING ACCOUNTS")
    print("="*80)
    
    accounts_dir = 'accounts'
    
    if not os.path.exists(accounts_dir):
        print(f"  ℹ️ Accounts directory not found: {accounts_dir}")
        return 0
    
    # List all account files
    all_accounts = [f for f in os.listdir(accounts_dir) if f.endswith('.txt')]
    
    if not all_accounts:
        print("  ℹ️ No accounts found")
        return 0
    
    # Filter by pattern if provided
    if pattern:
        import fnmatch
        accounts_to_delete = [f for f in all_accounts if fnmatch.fnmatch(f.replace('.txt', ''), pattern)]
        print(f"  📋 Found {len(accounts_to_delete)} account(s) matching '{pattern}':")
    else:
        accounts_to_delete = all_accounts
        print(f"  ⚠️ WARNING: This will delete ALL {len(accounts_to_delete)} accounts!")
        print(f"  📋 Accounts:")
    
    # Display accounts
    for acc in accounts_to_delete[:10]:  # Show first 10
        print(f"     - {acc.replace('.txt', '')}")
    if len(accounts_to_delete) > 10:
        print(f"     ... and {len(accounts_to_delete) - 10} more")
    
    # Confirm deletion
    if not pattern:
        confirm = input("\n  ⚠️ Delete ALL accounts? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("  ❌ Cancelled")
            return 0
    
    # Delete accounts
    deleted = 0
    for acc_file in accounts_to_delete:
        try:
            os.remove(os.path.join(accounts_dir, acc_file))
            deleted += 1
        except Exception as e:
            print(f"  ✗ Failed to delete {acc_file}: {str(e)}")
    
    print(f"\n  ✓ Deleted {deleted}/{len(accounts_to_delete)} account(s)")
    return deleted


def display_current_state():
    """Display current system state"""
    print("\n" + "="*80)
    print("CURRENT SYSTEM STATE")
    print("="*80)
    
    # Check network registry
    registry_file = 'network_nodes.txt'
    if os.path.exists(registry_file):
        try:
            with open(registry_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    nodes = json.loads(content)
                    print(f"📊 Network Registry: {len(nodes)} node(s)")
                    for node_id, node_info in list(nodes.items())[:5]:
                        username = node_info.get('username', 'Unknown')
                        port = node_info.get('port', '?')
                        print(f"   - {username} (port {port})")
                    if len(nodes) > 5:
                        print(f"   ... and {len(nodes) - 5} more")
                else:
                    print(f"📊 Network Registry: Empty")
        except:
            print(f"📊 Network Registry: Corrupted or unreadable")
    else:
        print(f"📊 Network Registry: Not found")
    
    # Check accounts
    accounts_dir = 'accounts'
    if os.path.exists(accounts_dir):
        accounts = [f for f in os.listdir(accounts_dir) if f.endswith('.txt')]
        print(f"\n👤 Accounts: {len(accounts)} account(s)")
        for acc in accounts[:5]:
            print(f"   - {acc.replace('.txt', '')}")
        if len(accounts) > 5:
            print(f"   ... and {len(accounts) - 5} more")
    else:
        print(f"\n👤 Accounts: Directory not found")
    
    # Check ports
    print(f"\n🔌 Checking ports 5000-5010...")
    busy_ports = []
    
    try:
        if os.name == 'nt':
            result = subprocess.run(
                ['netstat', '-ano'],
                capture_output=True,
                text=True,
                timeout=5
            )
            for port in range(5000, 5011):
                if f':{port}' in result.stdout and 'LISTENING' in result.stdout:
                    busy_ports.append(port)
        else:
            for port in range(5000, 5011):
                result = subprocess.run(
                    ['lsof', '-ti', f':{port}'],
                    capture_output=True,
                    text=True,
                    timeout=1
                )
                if result.stdout.strip():
                    busy_ports.append(port)
    except:
        print("   ⚠️ Could not check ports")
    
    if busy_ports:
        print(f"   Busy ports: {', '.join(map(str, busy_ports))}")
    else:
        print(f"   All ports clear")


def main():
    """Main cleanup function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Cleanup utility for blockchain system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cleanup.py --all              # Full cleanup (ports + registry)
  python cleanup.py --ports            # Kill processes only
  python cleanup.py --registry         # Clear registry only
  python cleanup.py --accounts         # Delete ALL accounts (dangerous!)
  python cleanup.py --malicious        # Delete only Malicious_* accounts
        """
    )
    
    parser.add_argument('--ports', action='store_true', help='Kill processes on ports')
    parser.add_argument('--registry', action='store_true', help='Clear network registry')
    parser.add_argument('--accounts', action='store_true', help='Delete ALL accounts')
    parser.add_argument('--malicious', action='store_true', help='Delete Malicious_* accounts only')
    parser.add_argument('--all', action='store_true', help='Full cleanup (ports + registry)')
    parser.add_argument('--status', action='store_true', help='Show current state only')
    
    args = parser.parse_args()
    
    # If no args, show interactive menu
    if not any(vars(args).values()):
        print("\n" + "🧹"*40)
        print("BLOCKCHAIN SYSTEM CLEANUP UTILITY")
        print("🧹"*40)
        
        # Show current state
        display_current_state()
        
        print("\n" + "="*80)
        print("CLEANUP OPTIONS")
        print("="*80)
        print("1. Kill processes on ports (5000-5100)")
        print("2. Clear network registry")
        print("3. Delete Malicious_* accounts only")
        print("4. Delete ALL accounts (⚠️ WARNING: deletes all user data!)")
        print("5. Full cleanup (1 + 2)")
        print("6. Show current state")
        print("0. Exit")
        
        choice = input("\nSelect option (0-6): ").strip()
        
        if choice == '1':
            kill_processes_on_ports()
        elif choice == '2':
            clear_network_registry()
        elif choice == '3':
            clear_accounts(pattern='Malicious_*')
        elif choice == '4':
            clear_accounts()
        elif choice == '5':
            kill_processes_on_ports()
            clear_network_registry()
        elif choice == '6':
            display_current_state()
        elif choice == '0':
            print("\n👋 Goodbye!")
            return
        else:
            print("\n❌ Invalid option!")
            return
    
    # Handle command line args
    else:
        if args.status:
            display_current_state()
        
        if args.all:
            kill_processes_on_ports()
            clear_network_registry()
        else:
            if args.ports:
                kill_processes_on_ports()
            if args.registry:
                clear_network_registry()
            if args.malicious:
                clear_accounts(pattern='Malicious_*')
            if args.accounts:
                clear_accounts()
    
    print("\n" + "="*80)
    print("✅ CLEANUP COMPLETE")
    print("="*80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
