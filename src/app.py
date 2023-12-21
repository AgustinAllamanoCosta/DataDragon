
# from src.api.service import Service
# from src.api.scan_service import ScanNode
# from src.api.socket_client import SocketClient
# from flask import Flask

# from api.socket_client import my_message

# app = Flask(__name__)
# service = Service()
# scan_service = ScanNode()
# socker_service = SocketClient(service)

# my_message("hello world")

# @app.route("/healthcheck/")
# def read_root():
#     return service.run_helath_check_test()

# @app.route("/")
# def node_data():
#     return service.get_node_data()

# @app.route("/prove")
# async def proove_data(in_file):
#     print(in_file)
    # proof_receive_path = "/src/zkp/examples/ziggy/proof-receive.json"
    # async with aiofiles.open(proof_receive_path, 'wb') as out_file:
    #     while content in await in_file.read(1024):
    #         await out_file.write(content)
    #     validation = service.validate()
    #     os.remove(proof_receive_path) 
    #     return validation

