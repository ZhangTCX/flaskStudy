# -*- coding: utf-8 -*-

from flask import Flask, render_template, Markup, flash, redirect, url_for

app = Flask(__name__)
'''
了解即可，不建议修改，容易出现兼容问题
修改定界符号，默认是 {{  }}
app.jinja_env.variable_start_string = "[["
app.jinja_env.variable_end_string = "]]"
'''
'''
了解即可，不修改也不影响
#删除jinja2语句后的第一个空行
app.jinja_env.trim_blocks = True
#删除jinja2语句所在行之前的空格和制表符
app.jinja_env.lstrip_blocks = True
#修改静态文件的加载路径；默认是static
app.static_url_path = 'xxxx'
'''
app.secret_key = 'secret string'

user = {
    'username': 'zhangjh',
    'bio': '个人喜欢的电影和音乐',
    'tnumber': 1,
}

movies = [
    {'name': '肖申克的救赎', 'year': '1999'},
    {'name': '星际穿越', 'year': '2018'},
    {'name': '海上钢琴师', 'year': '2005'},
    {'name': '泰坦尼克号', 'year': '2001'},
    {'name': '最长的电影', 'year': '2007'},
    {'name': '泪桥', 'year': '2012'},
    {'name': '阿凡达', 'year': '2011'},
    {'name': '信条', 'year': '2022'},
    {'name': '哈利波特与魔法石', 'year': '2002'},
    {'name': '霍比特人3', 'year': '2023'},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)

@app.route('/show')
def show():
    return render_template('show.html', user=user)

@app.route('/about')
def about():
    return '<h1>Hello about!</h1><a href="/">&larr; Return</a>'

'''
app.context_processor  -- 自定义上下文
'''
#使用方式1
@app.context_processor
def inject_foo():
    return dict(foo="I am foo.")
#使用方式2
def inject_foo1():
    return {"foo1":"I am foo1."}
app.context_processor(inject_foo1)
#使用方式3(lambda)
app.context_processor(lambda : {"foo2":"I am foo2."})
#使用方式4
app.jinja_env.globals["foo3"] = "I am foo3."
'''
app.template_global  -- 自定义全局函数(入参name可以自定义名称)
'''
#方式1
@app.template_global('myBar')
def bar():
    return "I am bar."
#方式2
app.jinja_env.globals["myBar2"] = bar

'''
app.template_filter  -- 自定义过滤器(入参name可以自定义名称)
'''
#方式1
@app.template_filter("myMusical")
def musical(text):
    return text + Markup(' &#9835;')
#方式2
app.jinja_env.filters["myMusical2"] = musical

'''
app.template_test  -- 自定义测试器(入参name可以自定义名称)
'''
#方式1
@app.template_test('testBaz')
def baz(n):
    if n == "baz":
        return True
    return False
#方式2
app.jinja_env.tests["testBaz2"] = baz

'''
消息闪现
'''
@app.route('/flash')
def just_flash():
    flash("你好，我是闪电")
    return redirect(url_for("index"))

'''
自定义错误界面
'''
@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404
