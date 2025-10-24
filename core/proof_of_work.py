"""
Proof of Work implementation
"""
import hashlib
import time


class ProofOfWork:
    def __init__(self, difficulty=4):
        """
        Khởi tạo Proof of Work
        
        Args:
            difficulty (int): Độ khó (số lượng số 0 đầu hash)
        """
        self.difficulty = difficulty
        self.target = '0' * difficulty
    
    def mine(self, block):
        """
        Mine một block
        
        Args:
            block (Block): Block cần mine
        
        Returns:
            tuple: (hash, nonce, time_elapsed)
        """
        start_time = time.time()
        nonce = 0
        
        print(f"Mining with difficulty {self.difficulty}...")
        
        while True:
            block.nonce = nonce
            hash_result = block.calculate_hash()
            
            if hash_result[:self.difficulty] == self.target:
                elapsed_time = time.time() - start_time
                print(f"Block mined in {elapsed_time:.2f} seconds!")
                print(f"Hash: {hash_result}")
                print(f"Nonce: {nonce}")
                return hash_result, nonce, elapsed_time
            
            nonce += 1
            
            # Progress indicator
            if nonce % 100000 == 0:
                print(f"Tried {nonce} hashes...")
    
    @staticmethod
    def validate_proof(block, difficulty):
        """
        Validate Proof of Work của một block
        
        Args:
            block (Block): Block cần validate
            difficulty (int): Độ khó
        
        Returns:
            bool: True nếu hợp lệ
        """
        target = '0' * difficulty
        return block.hash[:difficulty] == target and block.hash == block.calculate_hash()
