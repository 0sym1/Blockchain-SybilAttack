"""
Transaction class - Đại diện cho một giao dịch trong blockchain
"""
import json
from datetime import datetime


class Transaction:
    def __init__(self, sender, receiver, amount, timestamp=None):
        """
        Khởi tạo giao dịch
        
        Args:
            sender (str): Địa chỉ người gửi
            receiver (str): Địa chỉ người nhận
            amount (float): Số lượng coin
            timestamp (float): Thời gian giao dịch
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp or datetime.now().timestamp()
    
    def to_dict(self):
        """Chuyển transaction thành dictionary"""
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
    
    def to_json(self):
        """Chuyển transaction thành JSON string"""
        return json.dumps(self.to_dict(), sort_keys=True)
    
    @staticmethod
    def from_dict(data):
        """Tạo Transaction từ dictionary"""
        return Transaction(
            sender=data['sender'],
            receiver=data['receiver'],
            amount=data['amount'],
            timestamp=data['timestamp']
        )
    
    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount} coins"
    
    def __repr__(self):
        return f"Transaction({self.sender}, {self.receiver}, {self.amount})"
