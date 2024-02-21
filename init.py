import database,topic_modeling
import app as flask_app
if __name__ == '__main__':
    with flask_app.app.app_context():  # 在上下文环境中初始化数据库
        db_app = database.init_app(flask_app.app, init=True)
        flask_app.session.clear()

    print('开始下载NTLK数据')
    topic_modeling.nltk.download('averaged_perceptron_tagger')
    print('初始化完成，可以启动Flask！')