from flask import Flask
from flask import render_template, redirect, request, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os, time

app = Flask(__name__)

@app.get("/")
@app.get("/index")
def index():
    filelist = []
    for x in os.listdir("./uploads"):
        upload_time = os.path.getmtime("./uploads/"+x)
        filelist.append(dict(name = x, date = time.asctime(time.localtime(upload_time))))
    return render_template("index.html", filelist=filelist)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f= request.files['file']
        f.save(f"./uploads/{secure_filename(f.filename)}")
    return redirect(url_for('index'))

@app.get("/uploads/<path:name>")
def getUpload(name):
    return send_from_directory("./uploads", secure_filename(name))

@app.get("/<path:name>")
def getfile(name):
    return send_from_directory("./templates", name)

@app.get("/remove/<path:name>")
def deletefile(name):
    if name in os.listdir("./uploads"):
        os.remove(f"./uploads/{secure_filename(name)}")
    return redirect(url_for('index'))

