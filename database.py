from flask_sqlalchemy import SQLAlchemy
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

    # # 邮箱配置
    # MAIL_SERVER = "smtp.163.com"
    # MAIL_USE_SSL = True
    # MAIL_PORT = 465
    # MAIL_USERNAME = "hynever@163.com"
    # MAIL_PASSWORD = "1111111111111"
    # MAIL_DEFAULT_SENDER = "hynever@163.com"

    # # 缓存配置
    # CACHE_TYPE = "RedisCache"
    # CACHE_REDIS_HOST = "127.0.0.1"
    # CACHE_REDIS_PORT = 6379
    #
    # # Celery配置
    # # 格式：redis://:password@hostname:port/db_number
    # CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
    # CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
    #
    # AVATARS_SAVE_PATH = os.path.join(BaseConfig.UPLOAD_IMAGE_PATH,"avatars")


def init_app(app):
    db = SQLAlchemy(app)

    class User(db.Model):
        __tablename__ = 'user'  # 设置表名, 表名默认为类名小写
        id = db.Column(db.Integer, primary_key=True) # 设置主键, 默认自增
        username = db.Column(db.String(80), unique=True, nullable=False) # 设置字段名 和 唯一约束
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __repr__(self):
            return '<User %r>' % self.username


    db.create_all()

    new_user = User(username='john', email='john@example.com')
    db.session.add(new_user)
    db.session.commit()

    all_users = User.query.all()
    user = User.query.filter_by(username='john').first()
    print(all_users,"\n",user)