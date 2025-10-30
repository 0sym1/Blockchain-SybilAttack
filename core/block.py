"""
Block class - Đại diện cho một block trong blockchain
"""
import hashlib
import json
from datetime import datetime
from .transaction import Transaction


class Block:
    def __init__(self, index, transaction, previous_hash, timestamp=None, nonce=0, miner=None):
        """
        Khởi tạo block
        
        Args:
            index (int): Vị trí của block trong chain
            transaction (Transaction): Giao dịch trong block
            previous_hash (str): Hash của block trước đó
            timestamp (float): Thời gian tạo block
            nonce (int): Số dùng để mining (Proof of Work)
            miner (str): Địa chỉ của miner (nhận mining reward)
        """
        self.index = index
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.timestamp = timestamp or datetime.now().timestamp()
        self.nonce = nonce
        self.miner = miner  # ✅ NEW: Lưu thông tin miner
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Tính hash của block"""
        block_string = json.dumps({
            'index': self.index,
            'transaction': self.transaction.to_dict() if self.transaction else None,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'miner': self.miner  # ✅ Include miner in hash
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """
        Mine block với Proof of Work
        
        Args:
            difficulty (int): Độ khó (số lượng số 0 đầu hash)
        """
        target = '0' * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"Block mined: {self.hash}")
    
    def to_dict(self):
        """Chuyển block thành dictionary"""
        return {
            'index': self.index,
            'transaction': self.transaction.to_dict() if self.transaction else None,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'hash': self.hash,
            'miner': self.miner  # ✅ Include miner
        }
    
    @staticmethod
    def from_dict(data):
        """Tạo Block từ dictionary"""
        transaction = None
        if data.get('transaction'):
            transaction = Transaction.from_dict(data['transaction'])
        
        block = Block(
            index=data['index'],
            transaction=transaction,
            previous_hash=data['previous_hash'],
            timestamp=data['timestamp'],
            nonce=data['nonce'],
            miner=data.get('miner')  # ✅ Load miner
        )
        block.hash = data['hash']
        return block
    
    def __str__(self):
        tx_str = str(self.transaction) if self.transaction else "No transaction"
        return f"Block #{self.index} [{self.hash[:10]}...] - {tx_str}"
    
    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash[:10]}...)"
