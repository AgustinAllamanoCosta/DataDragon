import os
import base64

from src.blockchain.blockchain import Blockchain
from flask import Flask, flash, request, redirect, url_for, send_from_directory, abort, send_file, render_template, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'src/endpoint/data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

MEGABYTE = 1_000_000
CHUNK = 4

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

blockchain = Blockchain()

@app.route("/")
def home():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_data = file.read()
            file_size = len(file_data)

            chunk_index = 0
            for i in range(0, file_size, CHUNK):
              if i + CHUNK > file_size:
                file_data_chunk = file_data[i:]
              else:
                file_data_chunk = file_data[i: i + CHUNK]
              encoded_file_data_chunk = base64.b64encode(file_data_chunk)
              blockchain.addBlock(encoded_file_data_chunk, chunk_index, file.filename)
              chunk_index += 1
    return render_template('upload.html')

@app.route('/explore')
def blockchain_explorer():
  return render_template('explore.html', blocks=Blockchain.toDictionary(blockchain.chain))

