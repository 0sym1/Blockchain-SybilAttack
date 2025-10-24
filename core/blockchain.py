"""
Blockchain class - Quản lý chuỗi các blocks
"""
import json
from .block import Block
from .transaction import Transaction
from datetime import datetime
import config


class Blockchain:
    def __init__(self, owner_address=None):
        """
        Khởi tạo blockchain với genesis block
        
        Args:
            owner_address (str): Địa chỉ của owner (nhận initial balance)
        """
        self.chain = []
        self.pending_transactions = []
        self.difficulty = config.DIFFICULTY
        self.mining_reward = config.MINING_REWARD
        self.owner_address = owner_address
        
        # Tạo genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Tạo block đầu tiên trong blockchain với initial balance cho owner"""
        # Nếu có owner, tạo coinbase transaction cho initial balance
        if self.owner_address:
            genesis_transaction = Transaction(
                sender="System",
                receiver=self.owner_address,
                amount=config.INITIAL_BALANCE,
                timestamp=datetime.now().timestamp()
            )
        else:
            # Không có owner, tạo genesis transaction thông thường
            genesis_transaction = Transaction(
                sender="Genesis",
                receiver="System",
                amount=0,
                timestamp=datetime.now().timestamp()
            )
        
        genesis_block = Block(
            index=0,
            transaction=genesis_transaction,
            previous_hash="0",
            timestamp=datetime.now().timestamp()
        )
        
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        
        if self.owner_address:
            print(f"Genesis block created! {self.owner_address} received {config.INITIAL_BALANCE} coins")
        else:
            print("Genesis block created!")
    
    def get_latest_block(self):
        """Lấy block cuối cùng trong chain"""
        return self.chain[-1] if self.chain else None
    
    def add_transaction(self, transaction):
        """
        Thêm giao dịch vào pending pool (với validation)
        
        Args:
            transaction (Transaction): Giao dịch cần thêm
        
        Raises:
            ValueError: Nếu transaction không hợp lệ
        """
        # Skip validation cho System transactions (genesis, mining reward)
        if transaction.sender == "System" or transaction.sender == "Genesis":
            self.pending_transactions.append(transaction)
            print(f"System transaction added to pool: {transaction}")
            return
        
        # Validate sender balance (confirmed + pending để tránh double-spending)
        confirmed = self.get_balance(transaction.sender)
        pending = self.get_pending_balance(transaction.sender)
        available = confirmed + pending
        
        if available < transaction.amount:
            raise ValueError(
                f"Insufficient balance for {transaction.sender}! "
                f"Available: {available} (Confirmed: {confirmed}, Pending: {pending}), "
                f"Required: {transaction.amount}"
            )
        
        self.pending_transactions.append(transaction)
        print(f"Transaction added to pool: {transaction}")
    
    def mine_pending_transactions(self, miner_address):
        """
        Mine tất cả giao dịch pending
        
        Args:
            miner_address (str): Địa chỉ của miner
        
        Returns:
            Block: Block mới được mine (hoặc None nếu không có transaction)
        """
        if not self.pending_transactions:
            print("No transactions to mine!")
            return None
        
        # Lấy transaction đầu tiên (mỗi block chỉ chứa 1 transaction)
        transaction = self.pending_transactions.pop(0)
        
        # Tạo block mới
        new_block = Block(
            index=len(self.chain),
            transaction=transaction,
            previous_hash=self.get_latest_block().hash
        )
        
        print(f"Mining block {new_block.index}...")
        new_block.mine_block(self.difficulty)
        
        # Thêm block vào chain
        self.chain.append(new_block)
        
        # ✅ FIX: Tạo mining reward transaction và MINE NGAY trong block tiếp theo
        # Thay vì add vào pending (gây vòng lặp), ta sẽ tạo block reward riêng
        # Nhưng để đơn giản, ta ADD vào pending nhưng CHỈ khi có transaction thật
        # Reward chỉ được claim khi mine block có transaction của user
        
        # Chỉ thêm reward nếu transaction KHÔNG phải từ System (tránh reward cho reward)
        if transaction.sender != "System" and transaction.sender != "Genesis":
            reward_transaction = Transaction(
                sender="System",
                receiver=miner_address,
                amount=self.mining_reward
            )
            self.pending_transactions.append(reward_transaction)
            print(f"💰 Mining reward of {self.mining_reward} coins added to pending pool")
        
        print(f"Block {new_block.index} mined successfully!")
        return new_block
    
    def is_chain_valid(self):
        """
        Kiểm tra tính hợp lệ của blockchain
        
        Returns:
            bool: True nếu chain hợp lệ, False nếu không
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Kiểm tra hash của block hiện tại
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {i} has invalid hash!")
                return False
            
            # Kiểm tra liên kết với block trước
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {i} has invalid previous_hash!")
                return False
            
            # Kiểm tra Proof of Work
            if not current_block.hash.startswith('0' * self.difficulty):
                print(f"Block {i} doesn't meet difficulty requirement!")
                return False
        
        return True
    
    def replace_chain(self, new_chain):
        """
        Thay thế chain hiện tại bằng chain mới (nếu hợp lệ và dài hơn)
        
        Args:
            new_chain (list): Chain mới
        
        Returns:
            bool: True nếu chain được thay thế, False nếu không
        """
        if len(new_chain) <= len(self.chain):
            return False
        
        # Tạo blockchain tạm để validate
        temp_blockchain = Blockchain()
        temp_blockchain.chain = [Block.from_dict(block) for block in new_chain]
        
        if not temp_blockchain.is_chain_valid():
            print("Received chain is invalid!")
            return False
        
        print("Replacing chain with longer valid chain...")
        self.chain = temp_blockchain.chain
        return True
    
    def get_balance(self, address):
        """
        Tính số dư của một địa chỉ (CHỈ từ confirmed transactions trong chain)
        
        Args:
            address (str): Địa chỉ cần kiểm tra
        
        Returns:
            float: Số dư confirmed
        """
        balance = 0
        
        # Duyệt qua tất cả blocks trong chain (chỉ confirmed transactions)
        for block in self.chain:
            if block.transaction:
                if block.transaction.sender == address:
                    balance -= block.transaction.amount
                if block.transaction.receiver == address:
                    balance += block.transaction.amount
        
        # KHÔNG tính pending transactions (chưa confirmed)
        # Pending transactions chỉ được tính sau khi mine thành công
        
        return balance
    
    def get_pending_balance(self, address):
        """
        Tính số dư pending (chưa confirmed) của một địa chỉ
        
        Args:
            address (str): Địa chỉ cần kiểm tra
        
        Returns:
            float: Số dư pending
        """
        pending_balance = 0
        
        for tx in self.pending_transactions:
            if tx.sender == address:
                pending_balance -= tx.amount
            if tx.receiver == address:
                pending_balance += tx.amount
        
        return pending_balance
    
    def get_total_balance(self, address):
        """
        Tính tổng số dư (confirmed + pending) của một địa chỉ
        
        Args:
            address (str): Địa chỉ cần kiểm tra
        
        Returns:
            tuple: (confirmed_balance, pending_balance, total_balance)
        """
        confirmed = self.get_balance(address)
        pending = self.get_pending_balance(address)
        total = confirmed + pending
        
        return confirmed, pending, total
    
    def to_json(self):
        """Chuyển blockchain thành JSON string"""
        chain_data = [block.to_dict() for block in self.chain]
        return json.dumps(chain_data, indent=2)
    
    def to_list(self):
        """Chuyển blockchain thành list of dicts"""
        return [block.to_dict() for block in self.chain]
    
    @staticmethod
    def from_list(chain_data, owner_address=None):
        """
        Tạo Blockchain từ list of dicts
        
        Args:
            chain_data (list): Danh sách các block dưới dạng dict
            owner_address (str): Địa chỉ owner (optional)
        
        Returns:
            Blockchain: Blockchain object
        """
        # Tạo blockchain mới nhưng không tạo genesis block
        blockchain = Blockchain.__new__(Blockchain)
        blockchain.chain = []
        blockchain.pending_transactions = []
        blockchain.difficulty = config.DIFFICULTY
        blockchain.mining_reward = config.MINING_REWARD
        blockchain.owner_address = owner_address
        
        # Load các blocks từ data
        for block_data in chain_data:
            block = Block.from_dict(block_data)
            blockchain.chain.append(block)
        
        return blockchain
    
    def display_chain(self):
        """Hiển thị toàn bộ blockchain"""
        print("\n" + "="*80)
        print(f"BLOCKCHAIN (Length: {len(self.chain)}, Difficulty: {self.difficulty})")
        print("="*80)
        
        for block in self.chain:
            print(f"\nBlock #{block.index}")
            print(f"  Timestamp: {datetime.fromtimestamp(block.timestamp)}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Hash: {block.hash}")
            print(f"  Nonce: {block.nonce}")
            if block.transaction:
                print(f"  Transaction: {block.transaction}")
        
        print("\n" + "="*80)
        print(f"Chain is valid: {self.is_chain_valid()}")
        print(f"Pending transactions: {len(self.pending_transactions)}")
        print("="*80 + "\n")
