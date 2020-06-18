# 蓝图
from flask import render_template, current_app

from . import index_blu


@index_blu.route('/')
def index():
    return render_template('news/index.html')


# 浏览器在访问,在访问每个网站的时候,都会发送一个Get请求,向/favicon.ico地址获取logo
# app中提供了方法send_static_file,会自动寻找static静态文件下面的资源
@index_blu.route('/favicon.ico')
def get_web_logo():
    return current_app.send_static_file('news/favicon.ico')
