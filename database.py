from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from datetime import timedelta
import os

class BaseConfig:
    SECRET_KEY = "your secret key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    UPLOAD_IMAGE_PATH = os.path.join(os.path.dirname(__file__),"media")

    PER_PAGE_COUNT = 10

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/literaturesearch?charset=utf8mb4"
    # 缓存配置
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = 6379

    AVATARS_SAVE_PATH = os.path.join(BaseConfig.UPLOAD_IMAGE_PATH, "avatars")


def init_app(app):
    db = SQLAlchemy(app)
    # 删除所有继承自db.Model的表
    # db.drop_all()

    global User
    class User(db.Model):
        __tablename__ = 'user'  # 设置表名, 表名默认为类名小写
        id = db.Column(db.Integer, primary_key=True) # 设置主键, 默认自增
        username = db.Column(db.String(80), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False) # 设置字段名 和 唯一约束
        password = db.Column(db.String(120), nullable=False)
        # 执行print(实例)时返回的内容
        def __repr__(self):
            return '<User %r>' % self.username

    db.create_all()
    return db

def create_user(db_app, username:str, email:str, password:str):
    try:
        new_user = User(username=username, email=email, password=password)
        db_app.session.add(new_user)
        db_app.session.commit() # 提交更改
    except IntegrityError:
        db_app.session.rollback()
        return False, "创建用户失败，此邮箱已被注册"
    except Exception:
        # 处理其他异常情况
        db_app.session.rollback()
        return False, "注册失败，请稍后再试。"
    else: return True, "创建用户成功"

def querry_user(db_app, email:str):
    all_users = User.query.all()
    user = User.query.filter_by(email=email).first()
    print(all_users, "\n", user)

