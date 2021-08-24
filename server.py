import os
from flask import Flask, flash, request, redirect, render_template, url_for, send_from_directory, g
from werkzeug.utils import secure_filename
from localStoragePy import localStoragePy
from login_middleware import check_user_login
from functools import wraps

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/nedalerekat/Desktop/Py-Pro/static'
localStorage = localStoragePy('py-project', 'json')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_login():
    return localStorage.getItem('username')

def set_user(username):
    return localStorage.setItem('username', username)

def remove_user():
    localStorage.removeItem('username')

def get_all_img():
    return os.listdir("/Users/nedalerekat/Desktop/Py-Pro/static")

def upload_file(f):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

def handle_upload_file(files):
    f = files['file']
    if f and allowed_file(f.filename):
        upload_file(f)

def check_user_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if localStorage.getItem('username') is not None:
            print(localStorage.getItem('username') is not None, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            return f(*args, **kwargs)
        return redirect('login')
    return decorated_function

# ============================================

@app.route('/', methods=['GET'])
@check_user_login
def index():
    if request.method == 'GET':
        if is_login:
            basename = get_all_img()
            return render_template('index.html', names=basename)

@app.route('/login', methods=['GET', 'POST'])
def try_to_login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        set_user(request.form['username'])
        return redirect('/')
        
@app.route('/logout', methods=['GET'])
def logout_user():
    remove_user()
    return redirect('/login')

@app.route('/upload', methods=['GET', 'POST'])
def upload_img():
    if request.method == 'POST':
        if request.files:
            handle_upload_file(request.files)
            return redirect(request.url)
    if request.method == 'GET':
        return render_template('uploaded.html')


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

if __name__ == '__main__' :
    app.run(host="0.0.0.0", debug=True)

# export FLASK_APP=server
# $ flask run
#  * Running on http://127.0.0.1:5000/

# watchmedo auto-restart --patterns="*.py"  python ./server.py