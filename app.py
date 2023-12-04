from flask import Flask, session, render_template, request, jsonify

# 创建flask实例对象
app = Flask(__name__)

# 创建根路由
@app.route('/')
def home():
    if 'user_name' not in session:
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route('/index')
def index():
    pass

@app.route('/login')
def login():
    pass

@app.route('/register')
def register():
    pass

if __name__ == '__main__':
    app.run()
