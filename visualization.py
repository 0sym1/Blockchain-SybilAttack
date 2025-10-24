"""
Visualization tools - Hiển thị mạng và attack một cách trực quan
"""
import os


class NetworkVisualizer:
    """Visualize network topology"""
    
    @staticmethod
    def display_network_graph(network_manager, highlight_nodes=None):
        """
        Hiển thị graph của network (dạng ASCII art)
        
        Args:
            network_manager: NetworkManager instance
            highlight_nodes: List các node_id cần highlight
        """
        highlight_nodes = highlight_nodes or []
        nodes = network_manager.get_all_nodes()
        
        print("\n" + "="*80)
        print("NETWORK TOPOLOGY")
        print("="*80)
        
        for node in nodes:
            node_id = node['node_id']
            username = node['username']
            is_highlighted = node_id in highlight_nodes
            
            # Icon dựa trên loại node
            if 'Sybil' in username:
                icon = '🦹'  # Sybil node
            elif 'Malicious' in username:
                icon = '👿'  # Malicious node
            else:
                icon = '👤'  # Normal node
            
            # Highlight nếu cần
            if is_highlighted:
                print(f"\n  ⚠️ [TARGET] {icon} {username} ({node_id[:8]}...)")
            else:
                print(f"\n  {icon} {username} ({node_id[:8]}...)")
            
            print(f"     └─ {node['url']}")
        
        print("\n" + "="*80)
        print(f"Total nodes: {len(nodes)}")
        print(f"Highlighted: {len(highlight_nodes)}")
        print("="*80 + "\n")
    
    @staticmethod
    def display_attack_progress(phase, description, success=None):
        """
        Hiển thị tiến trình attack
        
        Args:
            phase: Tên phase
            description: Mô tả
            success: True/False/None
        """
        print("\n" + "─"*80)
        print(f"📍 {phase}")
        print("─"*80)
        print(f"   {description}")
        
        if success is True:
            print(f"   ✅ Success")
        elif success is False:
            print(f"   ❌ Failed")
        
        print("─"*80 + "\n")
    
    @staticmethod
    def display_chain_comparison(chains_dict):
        """
        So sánh nhiều blockchain
        
        Args:
            chains_dict: Dict {node_name: blockchain}
        """
        print("\n" + "="*80)
        print("BLOCKCHAIN COMPARISON")
        print("="*80)
        
        for node_name, blockchain in chains_dict.items():
            print(f"\n{node_name}:")
            print(f"  Length: {len(blockchain.chain)}")
            print(f"  Latest hash: {blockchain.get_latest_block().hash[:16]}...")
            print(f"  Pending txs: {len(blockchain.pending_transactions)}")
        
        print("\n" + "="*80 + "\n")
    
    @staticmethod
    def display_peer_connections(node, network_manager):
        """
        Hiển thị kết nối của một node
        
        Args:
            node: Node instance
            network_manager: NetworkManager instance
        """
        print("\n" + "="*80)
        print(f"PEER CONNECTIONS: {node.username}")
        print("="*80)
        print(f"Node: {node.username} ({node.get_url()})")
        print(f"Connected peers: {len(node.peers)}")
        print("─"*80)
        
        if not node.peers:
            print("  [No peers connected]")
        else:
            for peer_id, peer_url in node.peers.items():
                peer_info = network_manager.get_node(peer_id)
                if peer_info:
                    peer_name = peer_info['username']
                    
                    # Icon dựa trên loại peer
                    if 'Sybil' in peer_name or 'Malicious' in peer_name:
                        icon = '⚠️'
                    else:
                        icon = '✓'
                    
                    print(f"  {icon} {peer_name} ({peer_id[:8]}...) → {peer_url}")
                else:
                    print(f"  ? Unknown ({peer_id[:8]}...) → {peer_url}")
        
        print("="*80 + "\n")
    
    @staticmethod
    def display_attack_statistics(total_nodes, attacker_nodes, honest_nodes):
        """
        Hiển thị thống kê attack
        
        Args:
            total_nodes: Tổng số nodes
            attacker_nodes: Số nodes của attacker
            honest_nodes: Số honest nodes
        """
        attacker_ratio = (attacker_nodes / total_nodes * 100) if total_nodes > 0 else 0
        
        print("\n" + "="*80)
        print("ATTACK STATISTICS")
        print("="*80)
        print(f"Total Network Size:    {total_nodes} nodes")
        print(f"Honest Nodes:          {honest_nodes} nodes ({honest_nodes/total_nodes*100:.1f}%)")
        print(f"Attacker Nodes:        {attacker_nodes} nodes ({attacker_ratio:.1f}%)")
        print("─"*80)
        
        # Hiển thị bar chart
        print("\nNetwork Control:")
        honest_bar = '█' * int(honest_nodes / total_nodes * 50)
        attacker_bar = '█' * int(attacker_nodes / total_nodes * 50)
        
        print(f"Honest:   [{honest_bar:<50}] {honest_nodes/total_nodes*100:.1f}%")
        print(f"Attacker: [{attacker_bar:<50}] {attacker_ratio:.1f}%")
        
        print("─"*80)
        
        # Đánh giá mức độ nguy hiểm
        if attacker_ratio >= 50:
            print("⚠️ CRITICAL: Attacker controls majority of network!")
            print("   → Can manipulate consensus")
            print("   → Can perform 51% attack")
            print("   → Double-spending possible")
        elif attacker_ratio >= 33:
            print("⚠️ HIGH RISK: Attacker has significant control")
            print("   → Can disrupt consensus")
            print("   → Can isolate nodes (Eclipse attack)")
        elif attacker_ratio >= 20:
            print("⚠️ MODERATE RISK: Attacker has notable presence")
            print("   → Can influence some decisions")
            print("   → Limited attack capability")
        else:
            print("✓ LOW RISK: Attacker has limited control")
        
        print("="*80 + "\n")
    
    @staticmethod
    def display_eclipse_diagram(target_node, malicious_nodes):
        """
        Hiển thị sơ đồ Eclipse attack
        
        Args:
            target_node: Target node
            malicious_nodes: List malicious nodes
        """
        print("\n" + "="*80)
        print("ECLIPSE ATTACK DIAGRAM")
        print("="*80)
        print("\nBefore Attack:")
        print("  [Honest] ← → [Target] ← → [Honest]")
        print("     ↓                         ↓")
        print("  [Honest]                 [Honest]")
        
        print("\nAfter Attack:")
        print("  [Honest] ✗   [Target]   ✗ [Honest]")
        print("               ↙ ↓ ↓ ↘")
        print("           [👿]  [👿]  [👿]  [👿]")
        print("           Malicious Nodes Control All Connections")
        
        print("\n" + "─"*80)
        print(f"Target: {target_node.username}")
        print(f"Surrounded by: {len(malicious_nodes)} malicious nodes")
        print(f"All {len(target_node.peers)} connections controlled")
        print("="*80 + "\n")
    
    @staticmethod
    def display_transaction_flow(sender, receiver, amount, status="pending"):
        """
        Hiển thị flow của transaction
        
        Args:
            sender: Người gửi
            receiver: Người nhận
            amount: Số lượng
            status: Trạng thái (pending, mined, confirmed)
        """
        status_icon = {
            'pending': '⏳',
            'mined': '⛏️',
            'confirmed': '✅',
            'rejected': '❌'
        }.get(status, '?')
        
        print("\n" + "─"*80)
        print(f"TRANSACTION {status_icon} {status.upper()}")
        print("─"*80)
        print(f"  {sender} ──[ {amount} coins ]──> {receiver}")
        print("─"*80 + "\n")
    
    @staticmethod
    def clear_screen():
        """Clear screen"""
        os.system('cls' if os.name == 'nt' else 'clear')


class AnimationHelper:
    """Helper cho animation"""
    
    @staticmethod
    def progress_bar(current, total, width=50, label="Progress"):
        """
        Hiển thị progress bar
        
        Args:
            current: Giá trị hiện tại
            total: Giá trị tổng
            width: Chiều rộng bar
            label: Label
        """
        percent = current / total if total > 0 else 0
        filled = int(width * percent)
        bar = '█' * filled + '░' * (width - filled)
        
        print(f"\r{label}: [{bar}] {percent*100:.1f}%", end='', flush=True)
        
        if current >= total:
            print()  # New line when complete
    
    @staticmethod
    def spinner(message="Loading"):
        """
        Hiển thị spinner animation
        
        Args:
            message: Message to display
        """
        import itertools
        import time
        
        spinner_chars = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        
        for _ in range(20):  # 20 frames
            print(f"\r{message} {next(spinner_chars)}", end='', flush=True)
            time.sleep(0.1)
        
        print(f"\r{message} ✓")
    
    @staticmethod
    def countdown(seconds, message="Starting in"):
        """
        Countdown animation
        
        Args:
            seconds: Số giây
            message: Message
        """
        import time
        
        for i in range(seconds, 0, -1):
            print(f"\r{message} {i}...", end='', flush=True)
            time.sleep(1)
        
        print(f"\r{message} GO! ✓")


# Convenience functions
def visualize_network(network_manager, highlight_nodes=None):
    """Shortcut để visualize network"""
    NetworkVisualizer.display_network_graph(network_manager, highlight_nodes)


def visualize_attack_stats(total, attacker, honest):
    """Shortcut để visualize attack statistics"""
    NetworkVisualizer.display_attack_statistics(total, attacker, honest)


def visualize_eclipse(target, malicious):
    """Shortcut để visualize eclipse attack"""
    NetworkVisualizer.display_eclipse_diagram(target, malicious)
