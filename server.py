import os
from flask import Flask, flash, request, redirect, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/dev/Desktop/Py-Pro/static'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    basename = os.listdir("./static")
    print(basename, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    return render_template('index.html', names=basename)

@app.route("/hello")
def hello_world():
    return "<p> Hello, World! </p>"

@app.route('/upload', methods=['GET', 'POST'])
def upload_img():
    if request.method == 'POST':
        print("Hello >>>>>>>>>>>>>>>>>>> World")
        print(request)
        print("Hello >>>>>>>>>>>>>>>>>>> World")
        if request.files:
            print(request.files)
            print("Hello >>>>>>>>>>>>>>>>>>> World")
            f = request.files['file']
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(request.url)
                # return redirect(url_for('download_file', name=filename))

    return render_template('index.html')


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

if __name__ == '__main__' :
    app.run(host="0.0.0.0", debug=True)

# $ export FLASK_APP=hello
# $ flask run
#  * Running on http://127.0.0.1:5000/

# watchmedo auto-restart --patterns="*.py"  python ./server.py