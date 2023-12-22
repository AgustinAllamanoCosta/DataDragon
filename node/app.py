from src.api.scan_service import ScanNode
from src.api.socket_client import start_socket
from src.api.api import run
from threading import Thread

node_scaner = ScanNode()
thread = Thread(target=start_socket)
thread.start()
run()