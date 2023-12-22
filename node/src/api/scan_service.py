import requests
from src.api.configuration import IP_ADDR, KNOW_NODES
from time import sleep
from threading import Thread

class ScanNode(object):

    blocks = IP_ADDR.split('.')

    def __init__(self) -> None:
        thread = Thread(target=self.do_ping)
        thread.start()

    def do_ping(self) -> None:
        try:
            while True:
                sleep(5)
                for new_block in range(1,254):

                    ip_to_ping: str = '{0}.{1}.{2}.{3}'.format(
                        self.blocks[0],
                        self.blocks[1],
                        self.blocks[2],
                        new_block
                    
                    )
                    if ip_to_ping != IP_ADDR:

                        url = 'http://{0}:80/'.format(ip_to_ping)
                        try:
                            response = requests.get(url,timeout=5)
                            if not url in KNOW_NODES and response.status_code == 200:
                                KNOW_NODES.append(url)
                        except Exception as e:
                            print("Request Error", e)
        except Exception as e:
            print("Error pining",e)
