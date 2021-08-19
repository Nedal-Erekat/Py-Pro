import os
from flask import Flask, flash, request, redirect, render_template, url_for, send_from_directory, g
from werkzeug.utils import secure_filename
from login_middleware import check_user_login
from functools import wraps

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/nedalerekat/Desktop/Py-Pro/static'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_user_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.form or g.user:
            return f(*args, **kwargs)
        return render_template('login.html')
    return decorated_function



@app.route('/', methods=['GET', 'POST'])
@check_user_login
def index():
    g.user = request.form['username']
    basename = os.listdir("/Users/nedalerekat/Desktop/Py-Pro/static")
    return render_template('index.html', names=basename)

@app.route('/login', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        return redirect(request.url)
        

@app.route('/upload', methods=['GET', 'POST'])
def upload_img():
    if request.method == 'POST':
        if request.files:
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

# export FLASK_APP=server
# $ flask run
#  * Running on http://127.0.0.1:5000/

# watchmedo auto-restart --patterns="*.py"  python ./server.py