import uuid
from typing import List
import socket

DEFAULT_CHAIN_LENGTH: int = 3
NODE_ID: str = str(uuid.uuid4())
KNOW_NODES: List[str] = []
HOSTNAME = socket.gethostname()
IP_ADDR = socket.gethostbyname(HOSTNAME)