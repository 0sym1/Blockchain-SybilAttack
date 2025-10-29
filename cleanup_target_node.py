"""
Quick Cleanup for Target Node After Eclipse Attack

Usage:
    python cleanup_target_node.py <target_port>

Example:
    python cleanup_target_node.py 5000
"""

import sys
import requests


def cleanup_target_node(port=5000):
    """Cleanup dead peers on target node"""
    target_url = f"http://127.0.0.1:{port}"
    
    print(f"\n🧹 Cleaning up dead peers on target node (port {port})...")
    
    try:
        # Get current status
        print(f"\n📊 Checking current status...")
        response = requests.get(f"{target_url}/info", timeout=2)
        if response.status_code == 200:
            info = response.json()
            username = info.get('username', 'Unknown')
            peers_count = info.get('peers_count', 0)
            
            print(f"   Node: {username}")
            print(f"   Current peers: {peers_count}/8")
            
            if peers_count == 0:
                print(f"\n✅ No peers to cleanup!")
                return
        else:
            print(f"   ⚠️ Could not get node info")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        print(f"\n💡 Make sure node is running on port {port}")
        return
    
    # Cleanup dead peers
    print(f"\n🔧 Removing dead peers...")
    try:
        response = requests.post(f"{target_url}/cleanup_peers", timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            removed = result.get('removed_count', 0)
            remaining = result.get('remaining_peers', 0)
            
            print(f"\n✅ Cleanup successful!")
            print(f"   Removed: {removed} dead peer(s)")
            print(f"   Remaining: {remaining}/8 active peer(s)")
            print(f"   Available slots: {8 - remaining}/8")
            
            if removed > 0:
                print(f"\n💡 Next steps:")
                print(f"   1. In your node terminal, select option: 11 (Connect to peers)")
                print(f"   2. You will reconnect to legitimate nodes")
            else:
                print(f"\n✅ All peers are healthy!")
        else:
            print(f"   ❌ Cleanup failed (HTTP {response.status_code})")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")


def main():
    """Main function"""
    print("\n" + "🧹"*40)
    print("TARGET NODE CLEANUP UTILITY")
    print("After Eclipse Attack")
    print("🧹"*40)
    
    # Get port from command line
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"\n❌ Invalid port: {sys.argv[1]}")
            print(f"Usage: python cleanup_target_node.py <port>")
            return
    else:
        # Ask user for port
        port_input = input("\nEnter target node port (default: 5000): ").strip()
        if port_input:
            try:
                port = int(port_input)
            except ValueError:
                print(f"❌ Invalid port: {port_input}")
                return
        else:
            port = 5000
    
    # Run cleanup
    cleanup_target_node(port)
    
    print("\n" + "="*80)


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
