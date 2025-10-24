"""
User Manager - Quản lý đăng ký/đăng nhập người dùng
"""
import os
import json
import config
from core.blockchain import Blockchain


class UserManager:
    def __init__(self):
        """Khởi tạo User Manager"""
        self.accounts_dir = config.ACCOUNTS_DIR
        
        # Tạo thư mục accounts nếu chưa tồn tại
        if not os.path.exists(self.accounts_dir):
            os.makedirs(self.accounts_dir)
            print(f"Created accounts directory: {self.accounts_dir}")
    
    def get_account_file(self, username):
        """
        Lấy đường dẫn file tài khoản
        
        Args:
            username (str): Tên người dùng
        
        Returns:
            str: Đường dẫn file
        """
        return os.path.join(self.accounts_dir, f"{username}.txt")
    
    def account_exists(self, username):
        """
        Kiểm tra tài khoản đã tồn tại chưa
        
        Args:
            username (str): Tên người dùng
        
        Returns:
            bool: True nếu tồn tại
        """
        return os.path.exists(self.get_account_file(username))
    
    def register(self, username, password):
        """
        Đăng ký tài khoản mới
        
        Args:
            username (str): Tên người dùng
            password (str): Mật khẩu
        
        Returns:
            tuple: (success, message, blockchain_data)
        """
        # Validate input
        if not username or not password:
            return False, "Username and password cannot be empty!", None
        
        if ' ' in username:
            return False, "Username cannot contain spaces!", None
        
        # Kiểm tra tài khoản đã tồn tại
        if self.account_exists(username):
            return False, "Username already exists!", None
        
        # Tạo blockchain mới cho user với initial balance
        blockchain = Blockchain(owner_address=username)
        
        # Tạo dữ liệu tài khoản
        account_data = {
            'username': username,
            'password': password,
            'blockchain': blockchain.to_list(),
            'node_id': None,
            'created_at': blockchain.get_latest_block().timestamp
        }
        
        # Lưu vào file
        account_file = self.get_account_file(username)
        with open(account_file, 'w', encoding='utf-8') as f:
            json.dump(account_data, f, indent=2, ensure_ascii=False)
        
        print(f"Account created: {username}")
        return True, "Registration successful!", blockchain.to_list()
    
    def login(self, username, password):
        """
        Đăng nhập
        
        Args:
            username (str): Tên người dùng
            password (str): Mật khẩu
        
        Returns:
            tuple: (success, message, account_data)
        """
        # Kiểm tra tài khoản tồn tại
        if not self.account_exists(username):
            return False, "Username does not exist!", None
        
        # Đọc dữ liệu tài khoản
        account_file = self.get_account_file(username)
        with open(account_file, 'r', encoding='utf-8') as f:
            account_data = json.load(f)
        
        # Kiểm tra mật khẩu
        if account_data['password'] != password:
            return False, "Incorrect password!", None
        
        print(f"Login successful: {username}")
        return True, "Login successful!", account_data
    
    def update_account(self, username, blockchain_data=None, node_id=None):
        """
        Cập nhật thông tin tài khoản
        
        Args:
            username (str): Tên người dùng
            blockchain_data (list): Dữ liệu blockchain mới
            node_id (str): Node ID mới
        
        Returns:
            bool: True nếu thành công
        """
        if not self.account_exists(username):
            return False
        
        # Đọc dữ liệu hiện tại
        account_file = self.get_account_file(username)
        with open(account_file, 'r', encoding='utf-8') as f:
            account_data = json.load(f)
        
        # Cập nhật
        if blockchain_data is not None:
            account_data['blockchain'] = blockchain_data
        
        if node_id is not None:
            account_data['node_id'] = node_id
        
        # Lưu lại
        with open(account_file, 'w', encoding='utf-8') as f:
            json.dump(account_data, f, indent=2, ensure_ascii=False)
        
        return True
    
    def get_account_data(self, username):
        """
        Lấy dữ liệu tài khoản
        
        Args:
            username (str): Tên người dùng
        
        Returns:
            dict: Dữ liệu tài khoản (hoặc None)
        """
        if not self.account_exists(username):
            return None
        
        account_file = self.get_account_file(username)
        with open(account_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_accounts(self):
        """
        Liệt kê tất cả tài khoản
        
        Returns:
            list: Danh sách username
        """
        accounts = []
        
        for filename in os.listdir(self.accounts_dir):
            if filename.endswith('.txt'):
                username = filename[:-4]  # Remove .txt
                accounts.append(username)
        
        return accounts
    
    def delete_account(self, username):
        """
        Xóa tài khoản
        
        Args:
            username (str): Tên người dùng
        
        Returns:
            bool: True nếu thành công
        """
        if not self.account_exists(username):
            return False
        
        account_file = self.get_account_file(username)
        os.remove(account_file)
        print(f"Account deleted: {username}")
        return True
    
    def display_accounts(self):
        """Hiển thị danh sách tài khoản"""
        accounts = self.list_accounts()
        
        print("\n" + "="*80)
        print(f"REGISTERED ACCOUNTS (Total: {len(accounts)})")
        print("="*80)
        
        for username in accounts:
            account_data = self.get_account_data(username)
            chain_length = len(account_data['blockchain'])
            print(f"  - {username} (Chain length: {chain_length})")
        
        print("="*80 + "\n")
