"""
Peer Discovery - Tìm kiếm và kết nối với các peers
"""
import random
import requests
import config


class PeerDiscovery:
    def __init__(self, node):
        """
        Khởi tạo Peer Discovery
        
        Args:
            node (Node): Node hiện tại
        """
        self.node = node
        self.max_peers = config.MAX_PEERS
    
    def discover_peers(self, network_manager):
        """
        Tìm và kết nối với peers ngẫu nhiên
        
        Args:
            network_manager (NetworkManager): Network manager instance
        
        Returns:
            list: Danh sách peers đã kết nối
        """
        # Lấy số peers cần kết nối
        needed_peers = self.max_peers - len(self.node.peers)
        
        if needed_peers <= 0:
            print("Already connected to maximum peers")
            return []
        
        # Lấy random nodes từ network (exclude node hiện tại)
        available_nodes = network_manager.get_random_nodes(
            count=needed_peers,
            exclude_ids=[self.node.node_id] + list(self.node.peers.keys())
        )
        
        connected_peers = []
        
        for node_info in available_nodes:
            if self.connect_to_peer(node_info):
                connected_peers.append(node_info)
        
        return connected_peers
    
    def connect_to_peer(self, peer_info):
        """
        Kết nối với một peer
        
        Args:
            peer_info (dict): Thông tin peer
        
        Returns:
            bool: True nếu kết nối thành công
        """
        peer_id = peer_info['node_id']
        peer_url = peer_info['url']
        
        # Kiểm tra xem đã kết nối chưa
        if peer_id in self.node.peers:
            return False
        
        # Kiểm tra không tự kết nối với chính mình
        if peer_id == self.node.node_id:
            return False
        
        # Kiểm tra không kết nối với cùng URL (port)
        if peer_url == self.node.get_url():
            print(f"Skipped self connection: {peer_url}")
            return False
        
        try:
            # Ping peer để kiểm tra kết nối
            response = requests.get(f"{peer_url}/ping", timeout=2)
            
            if response.status_code == 200:
                # Thêm peer vào danh sách
                self.node.add_peer(peer_id, peer_url)
                print(f"Connected to peer: {peer_info['username']} ({peer_url})")
                
                # Thông báo cho peer về kết nối (optional)
                try:
                    requests.post(
                        f"{peer_url}/add_peer",
                        json={
                            'peer_id': self.node.node_id,
                            'peer_url': self.node.get_url()
                        },
                        timeout=2
                    )
                except:
                    pass
                
                return True
        except Exception as e:
            print(f"Failed to connect to {peer_url}: {str(e)}")
        
        return False
    
    def disconnect_peer(self, peer_id):
        """
        Ngắt kết nối với peer
        
        Args:
            peer_id (str): ID của peer
        """
        if peer_id in self.node.peers:
            peer_url = self.node.peers[peer_id]
            
            try:
                # Thông báo cho peer về việc ngắt kết nối
                requests.post(
                    f"{peer_url}/remove_peer",
                    json={'peer_id': self.node.node_id},
                    timeout=2
                )
            except:
                pass
            
            self.node.remove_peer(peer_id)
            print(f"Disconnected from peer: {peer_id}")
    
    def reconnect_peers(self, network_manager):
        """
        Kết nối lại các peers nếu số lượng giảm
        
        Args:
            network_manager (NetworkManager): Network manager instance
        """
        if len(self.node.peers) < self.max_peers:
            print(f"Reconnecting peers... (Current: {len(self.node.peers)}/{self.max_peers})")
            self.discover_peers(network_manager)
