from flask import Flask, session, render_template, request, jsonify, json
import hashlib
import logging, os
from flask_wtf import CSRFProtect

import database as db

# 创建flask实例对象
app = Flask(__name__, template_folder=r".\templates")
app.secret_key = os.urandom(24)
with open('session.txt', 'w') as f:
    f.write(str(app.secret_key))

app.config.from_object(db.DevelopmentConfig) # 配置数据库

with app.app_context():
    db_app = db.init_app(app) # 在上下文环境中初始化数据库
    # db.create_user(db_app, "John",'John@163.com', "John")

# 设置日志级别
app.logger.setLevel(logging.INFO)

# app.config['SECRET_KEY'] = 'your_secret_key'  # 设置一个用于加密表单令牌的密钥
# csrf = CSRFProtect(app) # 开启后使用post时会出现#400 bad request报错

# 判断当前用户是否在session中。由于flask要求命名空间映射唯一，所以使用functools模块动态生成装饰器函数
import functools
def if_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "user_name" in session:
            return func(*args, **kwargs)
        else:
            print("user not in session, redirecting to login")
            return render_template("login_register.html")
    return wrapper


# 创建根路由
@app.route('/')
@if_session
def home():
    return render_template('index.html')

@app.route('/index', methods=["GET", "POST"])
@if_session
def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        pass


@app.route('/login_register', methods=["GET", "POST"])
def login_register():
    if request.method == 'GET':
        return render_template('login_register.html')
    elif request.method == 'POST':
        data = request.json
        data['password'] = hashlib.sha256(data['password'].encode()).hexdigest()
        # print(data)
        if 'username' in data: # 为注册请求
            with app.app_context():
                res = db.create_user(db_app, data['username'], data['email'], data['password'])  # 在数据库中创建用户
            print(res)
            if res[0] == 200:
                # 创建session对象存储用户名，将用户名存储到 session 中
                session['user_name'] = data['username']
                return jsonify({'state': 200, "message": res[1]})
            else: return jsonify({'state': res[0], "message": res[1]})
        else: # 为登入请求
            with app.app_context():
                res = db.query_user(data['email'], data['password'])  # 在数据库中查找用户并核对密码
            print(res)
            if res[0] == 200:
                return jsonify({'state': 200})
            else:
                return jsonify({'state': res[0], 'message': res[1]})

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return render_template('login.html')


if __name__ == '__main__':
    logout()
    app.run(port=5000, debug=True)


