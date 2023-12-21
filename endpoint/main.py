import asyncio
import base64
import json
from typing import List
import websockets

from os import listdir

FILES_SENDED: List[str] = []
MEGABYTE = 1_000_000
CHUNK = 4

# async def start():
#   print("runing socket")
#   async with websockets.serve(send, "127.0.0.1", 8001):
#     await asyncio.Future()

# async def send(websocket):
#   while True:
#       data_path = "data"
#       print("reading files")
#       file_path = data_path + "/" + listdir(file_path)[0]

#       print("File path " + file_path)
#       with open(file_path) as file:
#         file_data = file.read()
#         file_size = len(file_data)

#         chunk_index = 0
#         print("file size " + file_size)
#         for i in range(0, file_size, CHUNK):
#           if i + CHUNK > file_size:
#             file_data_chunk = file_data[i:]
#           else:
#             file_data_chunk = file_data[i: i + CHUNK]
#           encoded_file_data_chunk = base64.b64encode(file_data_chunk)
#           data_to_stream = {
#             "chunk":encoded_file_data_chunk,
#             "index":chunk_index,
#             "filename":file.filename
#           }

#           print("sendingn chunks")
#           websocket.send(json.dumps(data_to_stream))
#           chunk_index += 1

# if __name__ == "__main__":
#     asyncio.run(start())

import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('fileData')
def test(sid, data):
    print(data)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5001)), app)