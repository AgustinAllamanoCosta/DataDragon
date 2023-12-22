import base64
import eventlet
import socketio
from typing import List

FILES_SENDED: List[str] = []
CHUNK = 4

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

def send_periodic_message():
    while True:
        try:
            data_path = "data"
            file_path = "/endpoint/data/hello.txt"
            with open(file_path) as file:
                file_data = file.read()
                file_size = len(file_data)
                chunk_index = 0
            for i in range(0, file_size, CHUNK):
                if i + CHUNK > file_size:
                    file_data_chunk = file_data[i:]
                else:
                    file_data_chunk = file_data[i: i + CHUNK]
                encoded_file_data_chunk = base64.b64encode(file_data_chunk.encode())
                data_to_stream = {
                    "chunk":str(encoded_file_data_chunk),
                    "index":chunk_index,
                    "filename":"hello.txt"
                }                
                sio.sleep(2)
                print("Emiiting")
                sio.emit('message', data_to_stream)
                chunk_index += 1
        except Exception as e:
            print(e)

if __name__ == '__main__':
    eventlet.spawn(send_periodic_message)
    eventlet.wsgi.server(eventlet.listen(('', 5001)), app)
