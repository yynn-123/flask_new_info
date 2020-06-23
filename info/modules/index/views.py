# 蓝图
from flask import render_template, current_app, session, request, jsonify

from info import constants
from info.models import User, News, Category
from info.utils.response_code import RET
from . import index_blu


@index_blu.route('/newslist')
def get_news_list():
    # 1、获取参数
    args_dict = request.args
    page = args_dict.get('p', 1)
    # 第几页
    # 一页多少数据
    per_page = args_dict.get('per_page', constants.HOME_PAGE_MAX_NEWS)
    # cid
    catagory_id = args_dict.get('cid', 1)
    # 2、校验参数
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.errot(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    filters = []
    # 3、查询数据并且分页
    if catagory_id != '1':
        filters.append(News.category_id == catagory_id)

    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
        # 获取查询的数据
        items = paginate.items
        # 获取总页数
        total_page = paginate.pages
        current_page = paginate.page
    except Exception as e:
        current_app.logger.errot(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询失败')
    news_li = []
    for new in items:
        news_li.append(new.to_basic_dict())
    # 4、返回数据
    return jsonify(errno=RET.OK, errmsg='OK', totalPage=total_page, currentPage=current_page, newsList=news_li,
                   cid=catagory_id)


@index_blu.route('/')
def index():
    """
    首页显示
    """
    # 获取当前登录用户的id
    user_id = session.get('user_id')
    # 通过id查询用户信息
    user = None
    news_list = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.errot(e)

    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.errot(e)
    click_news_list = []
    for news in news_list if news_list else []:
        click_news_list.append(news.to_basic_dict())

    """
    获取新闻分类数据
    """
    catagories_dicts = []
    catagories = Category.query.all()
    for catagory in catagories:
        catagories_dicts.append(catagory.to_dict())
    data = {
        'user_info': user.to_dict() if user else None,
        'click_news_list': click_news_list,
        'catagories': catagories_dicts
    }
    return render_template('news/index.html',
                           data=data
                           )


# 浏览器在访问,在访问每个网站的时候,都会发送一个Get请求,向/favicon.ico地址获取logo
# app中提供了方法send_static_file,会自动寻找static静态文件下面的资源
@index_blu.route('/favicon.ico')
def get_web_logo():
    return current_app.send_static_file('news/favicon.ico')
