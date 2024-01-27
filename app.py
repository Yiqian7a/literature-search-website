from flask import Flask, session, render_template, request, jsonify, json
import database as db
import logging
from flask_wtf import CSRFProtect

# 创建flask实例对象
app = Flask(__name__, template_folder=r".\templates")
app.config.from_object(db.DevelopmentConfig) # 配置数据库
with app.app_context():
    db.init_app(app) # 在上下文环境中初始化数据库

# 设置日志级别
app.logger.setLevel(logging.INFO)

app.config['SECRET_KEY'] = 'your_secret_key'  # 设置一个用于加密表单令牌的密钥
csrf = CSRFProtect(app)

# 判断当前用户是否在session中。由于flask要求命名空间映射唯一，所以用exec代替直接定义wrapper函数，结果是一样的
def if_session(func):
    func_name = func.__name__ + "_wrapper"
    print(f"wrapping function: {func_name}")
    exec("""
def {name}(*args, **kwargs):
    if "user_name" in session:
        return func(*args, **kwargs)
    else:
        print("user not in session, locate to login")
        return render_template("login_register.html")
    return {name}
""".format(name = func_name))
    return eval(func_name)

# 创建根路由
@app.route('/')
@if_session
def home():
    return render_template('index.html')

@app.route('/index', methods=["GET", "POST"])
# @if_session
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
        print(data)
        if 'username' in data: # 为注册请求
            return jsonify({'state': 200, "message": "注册成功"})
        else: # 为登入请求

            with open("./data/userdata.json", 'r') as f:
                userdata = json.load(f)
            if username in userdata and data['password'] == userdata[username]['password']:
                # 创建session对象存储用户名，将用户名存储到 session 中
                session['user_name'] = username[1:]
                return jsonify({'state': 200, "message": "登录成功"})
            elif username not in list(userdata):
                return jsonify({'state': 501, 'message': '用户未注册'})
            else:
                return jsonify({'state': 502, 'message': '用户名或密码错误'})

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(port=5000)

    # 删除所有继承自db.Model的表
    db.drop_all()