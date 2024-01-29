from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import os

from datetime import timedelta

class BaseConfig:
    SECRET_KEY = os.urandom(24) # 每次重启服务器都更换session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7) # session每7天过期

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_IMAGE_PATH = os.path.join(os.path.dirname(__file__),"media")

    PER_PAGE_COUNT = 10

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/literaturesearch?charset=utf8mb4"
    # 缓存配置
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = 6379

    AVATARS_SAVE_PATH = os.path.join(BaseConfig.UPLOAD_IMAGE_PATH, "avatars")


def init_app(app, init = False):
    db = SQLAlchemy(app)
    # 删除所有继承自db.Model的表
    # db.drop_all()

    global User, RSoE
    # 创建用户表单
    class User(db.Model):
        __tablename__ = 'user'  # 设置表名, 表名默认为类名小写
        id = db.Column(db.Integer, primary_key=True) # 设置主键, 默认自增
        username = db.Column(db.String(80), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False) # 设置字段名 和 唯一约束
        password = db.Column(db.String(120), nullable=False)
        # 执行print(实例)时返回的内容
        def __repr__(self):
            return '<User %r>' % self.username

    # 创建Remote Sensing of Environment期刊数据表单
    class RSoE(db.Model):
        __tablename__ = 'remote_sensing_of_environment'
        # all_title_list = [
        #     "PT", "AU", "AF", "TI", "SO", "LA", "DT", "DE", "ID", "AB", "C1", "C3", "EM", "OI",
        #     "FU", "FX", "NR", "TC", "Z9", "U1", "U2", "PU", "PI", "PA", "SN", "EI", "J9", "JI",
        #     "PD", "PY", "VL", "AR", "DI", "PG", "WC", "WE", "SC", "GA", "UT", "OA", "DA", "ER"
        # ]

        # 创建属性名
        global title_dict
        title_dict = {
            "AB": "摘要",
            "TI": "文献标题",
            "AU": "作者",
            "PG": "页数",
            "PY": "出版年",
            "PD": "出版日期",

            "WC": "类别",
            "SC": "研究方向",
            "NR": "引用的参考文献数",
            "U1": "被引用次数（最近 180 天）",
            "U2": "被引用次数（2013 年至今）",

            "CT": "会议标题",
            "CY": "会议日期",
            "CL": "会议地点",
            "SP": "会议赞助方",
            "HO": "会议主办方",

            "UT": "入藏号",
        }
        id = db.Column(db.Integer, primary_key=True)

        AB = db.Column(db.Text)
        TI = db.Column(db.Text)
        AU = db.Column(db.Text)
        PY = db.Column(db.Integer)
        PD = db.Column(db.Text)
        PG = db.Column(db.Integer)

        WC = db.Column(db.Text)
        SC = db.Column(db.Text)
        NR = db.Column(db.Integer)
        U1 = db.Column(db.Integer)
        U2 = db.Column(db.Integer)

        CT = db.Column(db.Text)
        CY = db.Column(db.Text)
        CL = db.Column(db.Text)
        SP = db.Column(db.Text)
        HO = db.Column(db.Text)

        UT = db.Column(db.String(20))

    db.create_all()

    # 写入数据
    if init:
        path = "./static/RSoE Data"
        for i in title_dict: title_dict[i] = ''
        for file in os.listdir(path):
            with open(path + "/" + file, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    if line != "\n":
                        # print(line[:-2])
                        if len(line) >= 4:
                            ti = line[:2]
                            if ti in title_dict:
                                title = str(ti)
                                title_dict[title] = line[3:]
                                same_title = True
                            elif ti == '  ' and same_title:
                                title_dict[title] += line[2:]
                            else: same_title = False
                    else: # 为空行，写入前一条文献的数据
                        # print(title_dict)
                        db.session.add(RSoE(**title_dict))
                        db.session.commit()
                        # 清空前一条文献的数据
                        for i in title_dict:
                            title_dict[i] = ''
        print("数据库初始化完成")
    return db

def create_user(db_app, username:str, email:str, password:str):
    try:
        new_user = User(username=username, email=email, password=password)
        db_app.session.add(new_user)
        db_app.session.commit() # 提交更改
    except IntegrityError:
        db_app.session.rollback()
        return 403, "创建用户失败，此邮箱已被注册"
    except SQLAlchemyError as e:
        db_app.session.rollback()
        return 500, f"注册失败，数据库错误: {str(e)}"
    except Exception as e:
        db_app.session.rollback()
        return 500, f"注册失败，未知错误: {str(e)}"
    else: return 201, "创建用户成功！"

def query_user(email:str ,password:str):
    if user := User.query.filter_by(email=email).first():
        print(user)
        if user.password == password:
            return 200, "登入成功", user
        else: return 403, '用户名或密码错误', user
    else: return 403, '用户不存在', user

def query_literature(start,end):
    res = RSoE.query.filter(RSoE.id.between(start, end)).all()
    print(res)
    return res

def search_literature(id = False,AU = False, TI = False):
    res = False
    if id:
        res = User.query.filter_by(id = id).first()
    if AU:
        res = RSoE.query.filter(RSoE.AU.like(f'%{AU}%')).all()
    if TI:
        res = RSoE.query.filter(RSoE.TI.like(f'%{TI}%')).all()

    return res