from flask import Flask, session, render_template, request, jsonify
import hashlib, random
import logging

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

with app.app_context(): # 在上下文环境中初始化数据库
    db_app = db.init_app(app, init = False)
    # First deploy should make the ↑ var:'init' True. 第一次部署应该将上一句init参数改为Ture
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
        if "user_name" in session:
            return func(*args, **kwargs)
        else:
            print("user not in session, redirecting to login")
            return render_template("login_register.html")
    return wrapper

def create_session(id:int, name:str, email:str):
    session['user_email'] = email
    session['user_name'] = name
    session['user_id'] = id


# 创建根路由
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index', methods=["GET", "POST"])
@if_session
def index():
    if request.method == "GET":
        # 随机返回5个文献
        res = []
        for i in range(5):
            random_id = random.randint(1, db.RSoE_num)
            res += db.search_literature(doc_id=random_id)
        return render_template('index.html', literatureData=res, username=session['user_name'])
    elif request.method == "POST":
        pass


@app.route('/login_register', methods=["GET", "POST"])
def login_register():
    if request.method == 'GET':
        return render_template('login_register.html')
    elif request.method == 'POST':
        data = request.json
        print(data)


        data['password'] = hashlib.sha256(data['password'].encode()).hexdigest()
        if 'username' in data: # 为注册请求
            if data['username'] == '' or data['email'] == '' or data['password'] == '':
                return jsonify({'state': 403, "message": '注册用户名、邮箱、密码不能为空'})
            # with app.app_context():
            res = db.create_user(db_app, data['username'], data['email'], data['password'])  # 在数据库中创建用户
            print(res)
            if res[0] == 201:
                # 创建session对象存储用户名，将用户名存储到 session 中
                create_session(id = res[2].id, name=res[2].name, email = res[2].email)
                return jsonify({'state': 201, "message": res[1]})
            else: return jsonify({'state': res[0], "message": res[1]})

        else: # 为登入请求
            if data['email'] == '' or data['password'] == '':
                return jsonify({'state': 403, "message": '登入邮箱、密码不能为空'})
            # with app.app_context():
            res = db.query_user(email = data['email'])  # 在数据库中查找用户并核对密码
            print(res)
            if res[0]:
                if res[1].password == data['password']:
                    create_session(id = res[1].id, name=res[1].name, email = res[1].email)
                    return jsonify({'state': 200, "message": "登入成功"})
                else:
                    return jsonify({'state': 403, 'message': '用户名或密码错误'})
            else:
                return jsonify({'state': 403, 'message':'用户不存在'})

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login_register.html')

# 在搜索框输入时调用
@app.route('/search', methods = ['POST'])
@if_session
def search():
    search_key = request.json['search_key']
    res = db.search_literature()

    return jsonify({'state': 200, 'res': res})

# 翻页的时候调用?
@app.route('/query', methods = ['POST'])
@if_session
def query_literature():
    data = request.json
    res = db.query_literature(data['start'],data['end'])
    if res:
        return jsonify({'state': 200, 'res': res})
    else: return jsonify({'state': 200, 'res': jsonify({"没有查询到相关结果"})})

@app.route('/detailed_information', methods = ['GET', 'POST'])
@if_session
def detailed_information():
    if request.method == 'GET':
        doc_id = request.args.get('doc_id')
        # print(doc_id)
        db.add_history(db_app, session['user_id'], doc_id)
        res = db.search_literature(doc_id = doc_id)[0]
        # print(res)
        return render_template('detailed_information.html', details = jsonify(res), username=session['user_name'])
    elif request.method == 'POST':
        data = request.json
        res = db.search_literature(doc_id = data['doc_id'])
        if res:
            return jsonify({'state': 200, 'res': res})
        else: return jsonify({'state': 200, 'res': "未查询到相关结果"})

@app.route('/history', methods = ['GET', 'POST'])
@if_session
def history():
    if request.method == 'GET':
        his = db.query_history(user_id = session['user_id'])
        his_dict = {}
        for i in range(1, 21):
            his_dict[f'h{i}'] = eval(f'his.h{i}')
        return render_template('history.html', his_dict = jsonify(his_dict), username=session['user_name'])
    elif request.method == 'POST':
        data = request.json


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


