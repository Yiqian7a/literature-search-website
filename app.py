from flask import Flask, session, render_template, request, jsonify, json
import hashlib
import logging, os

import database as db

'''
报错信息表 = {
    200: 成功访问页面
    201: 成功创建信息
    403: 服务器拒绝请求
    500: 服务器内部错误
}
'''



# 创建flask实例对象
app = Flask(__name__)
app.config.from_object(db.DevelopmentConfig) # 配置app

with open('session.txt', 'w') as f:
    f.write(str(app.secret_key))

with app.app_context():
    db_app = db.init_app(app, init = False) # 在上下文环境中初始化数据库
    # db.create_user(db_app, "John",'John@163.com', "John") # test



# 设置日志级别
app.logger.setLevel(logging.INFO)

# from flask_wtf import CSRFProtect
# csrf = CSRFProtect(app) # 开启后使用post时会出现#400 bad request报错

# 判断当前用户是否在session中。由于flask要求命名空间映射唯一，所以使用functools模块动态生成装饰器函数
import functools
def if_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "username" in session:
            return func(*args, **kwargs)
        else:
            print("user not in session, redirecting to login")
            return render_template("login_register.html")
    return wrapper


# 创建根路由
@app.route('/')
# @if_session
def home():
    return render_template('home.html')

@app.route('/index', methods=["GET", "POST"])
@if_session
def index():
    if request.method == "GET":

        return render_template('index.html', username = session['username'])
    elif request.method == "POST":
        pass


@app.route('/login_register', methods=["GET", "POST"])
def login_register():
    if request.method == 'GET':
        return render_template('login_register.html')
    elif request.method == 'POST':
        data = request.json
        print(data)
        if data['email'] == '' or data['password'] == '':
            return jsonify({'state': 403, "message": '登入邮箱、密码不能为空'})

        data['password'] = hashlib.sha256(data['password'].encode()).hexdigest()
        if 'username' in data: # 为注册请求
            if data['username'] == '':
                return jsonify({'state': 403, "message": '用户名不能为空'})
            with app.app_context():
                res = db.create_user(db_app, data['username'], data['email'], data['password'])  # 在数据库中创建用户
            print(res)
            if res[0] == 201:
                # 创建session对象存储用户名，将用户名存储到 session 中
                session['email'] = data['email']
                session['username'] = data['username']
                return jsonify({'state': 201, "message": res[1]})
            else: return jsonify({'state': res[0], "message": res[1]})

        else: # 为登入请求
            with app.app_context():
                res = db.query_user(data['email'], data['password'])  # 在数据库中查找用户并核对密码
            print(res)
            if res[0] == 200:
                session['email'] = data['email']
                session['username'] = res[2].username
                return jsonify({'state': 200})
            else:
                return jsonify({'state': res[0], 'message': res[1]})

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login_register.html')

@app.route('/search', methods = ['POST'])
@if_session
def search():
    data = request.json
    res = db.search_literature()
    return jsonify({'state': 200, 'res': res})

@app.route('/query', methods = ['POST'])
@if_session
def query_literature():
    data = request.json
    res = db.query_literature(data['start'],data['end'])
    if res != {}:
        return jsonify({'state': 200, 'res': res})
    else: return jsonify({'state': 200, 'res': "未查询到相关结果"})

@app.route('/detailed_information', methods = ['GET', 'POST'])
@if_session
def detailed_information():
    if request.method == 'GET':
        return render_template('detailed_information.html')
    data = request.json
    res = db.search_literature(id = data['id'])
    if res != {}:
        return jsonify({'state': 200, 'res': res})
    else: return jsonify({'state': 200, 'res': "未查询到相关结果"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


