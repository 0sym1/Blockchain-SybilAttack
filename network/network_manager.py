"""
Network Manager - Quản lý danh sách tất cả nodes trong mạng
"""
import json
import os
import config


class NetworkManager:
    def __init__(self):
        """Khởi tạo Network Manager"""
        self.network_file = config.NETWORK_FILE
        self.nodes = self.load_network()
    
    def load_network(self):
        """
        Load danh sách nodes từ file
        
        Returns:
            dict: Dictionary với key là node_id, value là node info
        """
        if not os.path.exists(self.network_file):
            return {}
        
        try:
            with open(self.network_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def save_network(self):
        """Lưu danh sách nodes vào file"""
        with open(self.network_file, 'w', encoding='utf-8') as f:
            json.dump(self.nodes, f, indent=2, ensure_ascii=False)
    
    def register_node(self, node_id, host, port, username):
        """
        Đăng ký node mới vào mạng
        
        Args:
            node_id (str): ID của node
            host (str): Host address
            port (int): Port number
            username (str): Tên người dùng
        """
        # Reload từ file để đảm bảo dữ liệu mới nhất
        self.nodes = self.load_network()
        
        # Kiểm tra và xóa nodes cũ của cùng username hoặc cùng port
        nodes_to_remove = []
        for existing_id, existing_node in self.nodes.items():
            if existing_node['username'] == username and existing_id != node_id:
                nodes_to_remove.append(existing_id)
                print(f"⚠️ Found duplicate username node: {existing_id[:8]}..., will remove")
            elif existing_node['port'] == port and existing_id != node_id:
                nodes_to_remove.append(existing_id)
                print(f"⚠️ Found duplicate port node: {existing_id[:8]}..., will remove")
        
        # Xóa các nodes trùng lặp
        for old_id in nodes_to_remove:
            self.unregister_node(old_id)
        
        # Đăng ký node mới
        self.nodes[node_id] = {
            'node_id': node_id,
            'host': host,
            'port': port,
            'username': username,
            'url': f"http://{host}:{port}",
            'is_active': True
        }
        self.save_network()
        print(f"Node {node_id[:8]}... registered to network")
    
    def unregister_node(self, node_id):
        """
        Xóa node khỏi mạng
        
        Args:
            node_id (str): ID của node
        """
        # Reload từ file để đảm bảo dữ liệu mới nhất
        self.nodes = self.load_network()
        
        if node_id in self.nodes:
            del self.nodes[node_id]
            self.save_network()
            print(f"Node {node_id} unregistered from network")
    
    def get_node(self, node_id):
        """
        Lấy thông tin một node
        
        Args:
            node_id (str): ID của node
        
        Returns:
            dict: Thông tin node
        """
        # Reload từ file để đảm bảo dữ liệu mới nhất
        self.nodes = self.load_network()
        return self.nodes.get(node_id)
    
    def get_all_nodes(self):
        """
        Lấy danh sách tất cả nodes
        
        Returns:
            list: Danh sách nodes
        """
        # Reload từ file để đảm bảo dữ liệu mới nhất
        self.nodes = self.load_network()
        return list(self.nodes.values())
    
    def get_active_nodes(self):
        """
        Lấy danh sách nodes đang hoạt động
        
        Returns:
            list: Danh sách active nodes
        """
        # Reload từ file để đảm bảo dữ liệu mới nhất
        self.nodes = self.load_network()
        return [node for node in self.nodes.values() if node.get('is_active', True)]
    
    def get_random_nodes(self, count, exclude_ids=None):
        """
        Lấy ngẫu nhiên một số nodes
        
        Args:
            count (int): Số lượng nodes cần lấy
            exclude_ids (list): Danh sách node_id không muốn lấy
        
        Returns:
            list: Danh sách nodes ngẫu nhiên
        """
        import random
        
        exclude_ids = exclude_ids or []
        available_nodes = [
            node for node in self.get_active_nodes()
            if node['node_id'] not in exclude_ids
        ]
        
        count = min(count, len(available_nodes))
        return random.sample(available_nodes, count)
    
    def mark_node_inactive(self, node_id):
        """
        Đánh dấu node là không hoạt động
        
        Args:
            node_id (str): ID của node
        """
        # Reload từ file để đảm bảo dữ liệu mới nhất
        self.nodes = self.load_network()
        
        if node_id in self.nodes:
            self.nodes[node_id]['is_active'] = False
            self.save_network()
    
    def mark_node_active(self, node_id):
        """
        Đánh dấu node là đang hoạt động
        
        Args:
            node_id (str): ID của node
        """
        # Reload từ file để đảm bảo dữ liệu mới nhất
        self.nodes = self.load_network()
        
        if node_id in self.nodes:
            self.nodes[node_id]['is_active'] = True
            self.save_network()
    
    def get_network_size(self):
        """
        Lấy số lượng nodes trong mạng
        
        Returns:
            int: Số lượng nodes
        """
        # Reload từ file để đảm bảo dữ liệu mới nhất
        self.nodes = self.load_network()
        return len(self.nodes)
    
    def display_network(self):
        """Hiển thị thông tin mạng"""
        # Reload từ file để đảm bảo dữ liệu mới nhất
        self.nodes = self.load_network()
        
        print("\n" + "="*80)
        print(f"NETWORK STATUS (Total Nodes: {self.get_network_size()})")
        print("="*80)
        
        for node in self.get_all_nodes():
            status = "🟢 ACTIVE" if node.get('is_active', True) else "🔴 INACTIVE"
            print(f"\n{status} {node['username']} ({node['node_id']})")
            print(f"  URL: {node['url']}")
        
        print("\n" + "="*80 + "\n")
