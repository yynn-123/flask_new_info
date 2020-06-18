import redis
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
app = Flask(__name__)

class Config(object):
    SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"
    # 工程信息配置
    DEBUG = True
    # 导入数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/information22'
    app.config['SQLALCHEMY_TRACK_MODUFICATIONS'] =  True
    app.config['SQLALCHEMY_ECHO'] = True


    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # flask_session配置信息
    SESSION_TYPE = "redis" # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用 redis 的实例
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 86400  # session 的有效期，单位是秒



app.config.from_object(Config)
db = SQLAlchemy(app)
# 初始化redis
redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
# 开启csrf保护，用于服务器验证
CSRFProtect(app)
# 设置session保存指定位置
Session(app)

manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)



@app.route('/')
def index():
    session['name'] = 'Albert'
    return 'index'
if __name__ == '__main__':
    manager.run()