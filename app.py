import os
from flask import Flask, render_template, request, redirect, url_for, abort, request
from werkzeug.utils import secure_filename
import subprocess
from colorama import *


app = Flask(__name__)

app.config['UPLOAD_EXTENSION_ONNX'] = ['.onnx']
app.config['UPLOAD_EXTENSION_VNNLIB'] = ['.vnnlib']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/",methods=['POST'])
def singleffn():
   uploadedOnnxFile = request.files['file1']
   onnxFilename = secure_filename(uploadedOnnxFile.filename)
   if onnxFilename != '':
        file_ext = os.path.splitext(onnxFilename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSION_ONNX']:
            abort(400,"Wrong .onnx file")
        uploadedOnnxFile.save(os.path.join(app.config['UPLOAD_PATH'], onnxFilename))
   uploadedVnnlibFile = request.files['file2']
   vnnlibFilename = secure_filename(uploadedVnnlibFile.filename)
   if vnnlibFilename != '':
        file_ext = os.path.splitext(vnnlibFilename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSION_VNNLIB']:
            abort(400,"Wrong .vnnlib file")
        uploadedVnnlibFile.save(os.path.join(app.config['UPLOAD_PATH'], vnnlibFilename))
   timeOut = request.form['timeout']
   actualmodel="uploads/"+onnxFilename
   propVnnlib="uploads/" + vnnlibFilename
   pythonProg="FFN.py " + actualmodel + " " +propVnnlib+"  "+timeOut
   output = subprocess.check_output("python3 " +pythonProg, shell=True)
   output=output.decode('utf8')
   return render_template('index.html',output=output)

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)

