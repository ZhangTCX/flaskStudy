# -*- coding : utf-8 -*-
import os
from flask import Flask, redirect, url_for, abort, make_response, json, jsonify, after_this_request, Markup
# Flask的程序上下文：current_app, g和请求上下文：request, session
from flask import current_app, g, request, session
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum
from datetime import timedelta
from jinja2 import escape

__author__ = "zhangjh"

app = Flask(__name__)

# 设置密钥 获取.env里面配置的密钥SECRET_KEY，如果没有则默认用第二个参数作为密钥
app.secret_key = os.getenv('SECRET_KEY', 'secret string')

# 指定cookie会话存储过期时间
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=30)  # 方便测试，30秒内重复登录都可以，30秒后就过期无法登录

# 所有路由
url_map = app.url_map


# http://192.168.1.103:8000/hello?name=zhangjh
@app.route('/')
@app.route('/hello', methods=['GET', 'POST'])  # 同时监听GET和POST请求
def hello():
    response = None
    name = request.args.get("name")
    if name is None:
        name = request.cookies.get("name", "Flask")  # 从Cookie中获取name值
        # response = "<h1>Hello, %s!</h1>" % escape(name)# escape对传入的数据进行转义，防止XSS攻击(2.0.0以上过时,被Markup.escape替代)
        response = "<h1>Hello, %s!</h1>" % Markup.escape(name)
    # 根据用户认证状态返回不同的内容 判断session
    if 'logged_in' in session:
        response += "[已登陆]"
    else:
        response += "[未登陆]"
    return response


@app.route('/goback/<int:year>')
def go_back(year):
    return 'Welcome to %d!' % (2022 - year)


# 相同route的会返回第一个
@app.route('/test1')
def test1():
    return "<h1>Hello, test1!</h1>"


@app.route('/test1')
def test2():
    return "<h1>Hello, test2!</h1>"


# 如果送的不是'blue','white','red'就会报404
colors = ['blue', 'white', 'red']


@app.route('/colors/<any(%s):color>' % str(colors)[1:-1])
def three_colors(color):
    return "<p>只能是蓝、白、红</p>"


'''
请求钩子(Hook)：
@app.before_first_request 注册一个函数，在处理第一个请求前运行  (flask2.0.0版本以上过时，替代方法是@app.before_startup )
@app.before_request 注册一个函数，在处理每个请求前运行
@app.after_request 注册一个函数，如果没有未处理的异常抛出，会在每个请求结束后运行(要接受响应类对象为参数)
@app.teardown_request 注册一个函数,即使有未处理的异常抛出，会在每个请求结束后运行。如果发生异常，会传入异常对象作为参数到注册的函数中(要接受异常对象为参数，正常处理时是None)
@after_this_request 在视图函数内注册一个函数，会在这个请求结束后运行(要接受响应类对象为参数)
'''


@app.before_first_request
def beforeFirstRequest():
    print("0.注册一个函数，在处理第一个请求前运行")


@app.before_request
def beforeRequest():
    print("1.注册一个函数，在处理每个请求前运行")

    @after_this_request
    def afterThisRequest(response):
        print("2.在视图函数内注册一个函数，会在这个请求结束后运行(要接受响应类对象为参数)")
        return response


@app.after_request
def afterRequest(response):
    print("3.注册一个函数，如果没有未处理的异常抛出，会在每个请求结束后运行(要接受响应类对象为参数)")
    return response


@app.teardown_request
def teardownRequest(exception):
    print("4.注册一个函数,即使有未处理的异常抛出，会在每个请求结束后运行。如果发生异常，会传入异常对象作为参数到注册的函数中(要接受异常对象为参数，正常处理时是None)")
    return exception


# 重定向 默认错误码302
@app.route('/rebacktobaidu')
def rebacktobaidu():
    return redirect("http://www.baidu.com", code=302)


# 重定向搭配url_for  要修改状态码就在redirect的第二个参数 或者 code关键字传入
@app.route('/gethello')
def gethello():
    return redirect(url_for('hello'), 303)


# 主动抛错abort() 不需要return abort()之后的代码不会被执行
@app.route('/404')
def not_found():
    abort(404)


'''
响应格式：
MIME类型：Flask提供的make_response()生成的响应对象，可使用响应对象的mimetype属性设置MIME类型
1、纯文本-text/plain 
2、HTML-text/html
3、XML-application/xml
4、JSON-application/json
'''


@app.route('/note', defaults={'content_type': 'text'})
@app.route('/note/<content_type>')
def note(content_type):
    response = None
    content_type = content_type.lower()
    if content_type == 'text':
        body = '''
                Note
                to: Peter
                from: Jane
                heading: Reminder
                body: Don't forget the party!
                '''
        response = make_response(body)
        response.mimetype = 'text/plain'
    elif content_type == 'html':
        body = '''
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
          <h1>Note</h1>
          <p>to: Peter</p>
          <p>from: Jane</p>
          <p>heading: Reminder</p>
          <p>body: <strong>Don't forget the party!</strong></p>
        </body>
        </html>
        '''
        response = make_response(body)
        response.mimetype = 'text/html'
    elif content_type == 'xml':
        body = '''<?xml version="1.0" encoding="UTF-8"?>
                  <note>
                      <to>Peter</to>
                      <from>Jane</from>
                      <heading>Reminder</heading>
                      <body>Don't forget the party!</body>
                  </note>
               '''
        response = make_response(body)
        response.mimetype = 'application/xml'
    elif content_type == 'json':
        body = {
            "note": {
                "to": "Peter",
                "from": "Jane",
                "heading": "Remider",
                "body": "Don't forget the party!"
            }
        }
        # equal to:
        # response = make_response(json.dumps(body))
        # response.mimetype = "application/json"
        # Flask提供了更方便的jsonify()函数
        response = jsonify(body)
    else:
        abort(400)
    return response


@app.route('/jsonf')
def jsonf():
    return jsonify(message='Error!'), 500  # 自定义返回状态码


'''
Cookie部分
'''


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


# session 将Cookie数据加密保存
# 模拟用户登陆
@app.route('/login')
def login():
    session['logged_in'] = True
    # 关键：标记为永久会话 会保留Cookie一段时间，由你的app.config['PERMANENT_SESSION_LIFETIME']指定
    session.permanent = True
    return redirect(url_for('hello'))


# 模拟后台登陆
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return "成功登陆后台"


# 模拟用户登出
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


'''
Flask上下文：
程序上下文：
    current_app：指向处理请求的当前程序实例
    g：替代Python的全局变量用法，确保仅在当前请求中可用。用于存储全局数据，每次请求都会重设
请求上下文：
    request：封装客户端发出的请求报文数据
    session：用于记住请求之间的数据，通过签名Cookie实现
'''


@app.before_request
def get_name():  # 其他函数就可以直接使用g.name获取对应的值
    g.name = request.args.get('name')
    print(f"g.name的值为{g.name}")


'''
http进阶实践部分
'''


# 重定向到上一个页面
@app.route('/foo')
def foo():
    href = url_for('do_something', next=request.full_path)
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' % href


@app.route('/bar')
def bar():
    href = url_for('do_something', next=request.full_path)
    return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' % href


@app.route('/do-something')
def do_something():
    return redirect_back()


def redirect_back(default='hello', **kwargs):
    # next一般为当前页面URL的查询参数
    # request.referrer记录用户原站点URL，很多情况下会是空值（浏览器自动清除）
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        elif is_safe_url(target):
            return redirect(target)
        return redirect(url_for(default, **kwargs))


# url安全验证 确保是程序内部url
def is_safe_url(target):
    ref_url = urlparse(request.host_url)  # 主机URL
    test_url = urlparse(urljoin(request.host_url, target))  # 将目标url转换为绝对URL
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# AJAX
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)  # 生成两段随机文本
    return '''
            <h1>A very long post</h1>
            <div class="body">%s</div>
            <button id="load">Load More</button>
            <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
            <script type="text/javascript">
            $(function() {
                $('#load').click(function() {
                    $.ajax({
                        url: '/more',                 // 目标URL
                        type: 'get',                  // 请求方法
                        success: function(data){      // 返回2XX响应后触发的回调函数
                            $('.body').append(data);  // 将返回的响应插入到页面中
                        }
                    })
                })
            })
            </script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)


'''
常见web端攻击：SQL注入、XSS攻击、CSRF攻击
'''
