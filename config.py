"""
Configuration file cho blockchain system
"""

# Blockchain Settings
DIFFICULTY = 4  # Số lượng số 0 đầu hash (độ khó mining)
MINING_REWARD = 10.0
INITIAL_BALANCE = 100.0  # Số dư ban đầu cho mỗi user mới
GENESIS_DATA = "Genesis Block - Blockchain Sybil Attack Demo"

# Network Settings
BASE_PORT = 5000
MAX_PEERS = 8  # Mỗi node kết nối tối đa 8 peers
NETWORK_DISCOVERY_INTERVAL = 30  # seconds

# Account Settings
ACCOUNTS_DIR = "accounts"
NETWORK_FILE = "network_nodes.txt"

# Attack Simulation Settings
SYBIL_NODES_COUNT = 20  # Số lượng node giả mạo trong Sybil attack
ECLIPSE_MALICIOUS_NODES = 8  # Số node độc hại cần để eclipse một node
