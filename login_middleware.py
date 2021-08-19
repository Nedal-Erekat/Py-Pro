from flask import Response, request, g, render_template
from functools import wraps

def check_user_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = request
        password = request
        print(request.form, '>>>>>>>>>>>>>>>>')
        if username == None or password == None:
            print('checked user')
            return f(*args, **kwargs)
        
        print('it is not checked user')
        return render_template('login.html')

    return decorated_function