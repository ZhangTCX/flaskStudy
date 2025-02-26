# -*- coding : utf-8 -*-
import os
from flask import Flask, render_template, Markup, flash, redirect, url_for

__author__ = "zhangjh"

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')

user = {
    'username': 'zhangjh',
    'bio': '本人的电影清单',
    'with_context': 1
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/watchlist')
def watchlist():
    return render_template("watchlist.html", user=user, movies=movies)

@app.route('/watchlist_styles')
def watchlist_styles():
    return render_template('watchlist_styles.html', user=user, movies=movies)

"""
内置上下文变量(Flask提供)
config 当前配置对象
request 当前的请求对象，在已激活的请求环境下可用
session 当前的会话对象，在已激活的请求环境下可用
g 与请求绑定的全局变量，在已激活的请求环境下可用

自定义上下文
当我们调用render_template()函数渲染任意模板时候，
所有使用app.context_processor装饰器注册的函数都会被执行,
这些返回值会被添加到模板中，因此我们可以在模板中直接使用。
(字符串，列表，函数，类或类实例)
"""
@app.context_processor
def inject_foo1():
    """
    第一种用法
    """
    foo = 'foo'
    return dict(foo=foo)  # 等同于 return {'foo':foo}

def inject_foo2():
    """
    第二种用法
    """
    eoo = 'eoo'
    return dict(eoo=eoo)
app.context_processor(inject_foo2)

"""
第三种用法：lambda写法
"""
app.context_processor(lambda: {"uoo": "baz"})

'''
内置全局函数(Jinja2提供)
http://jinja.pocoo.org/docs/2.10/templates/#list-of-global-functions   --完整的全局函数列表查看地址
一般循环和字典这些都和Python当中使用一样

内置全局函数(Flask提供)
url_for() 用于生成URL的函数
get_flashed_messages() 用于获取flash消息的函数

自定义全局函数
在模板可以直接{{ bar() }}进行使用
app.template_global(name) 可以自定义名称 
如：@app.template_global('barr') 那么在模板就是{{ barr() }}进行使用
'''
@app.template_global()
def bar():
    return '测试bar.'
# 也可以这样添加：app.jinja_env.globals['bar'] = bar

'''
内置过滤器(Jinja2提供)
使用方式1：{{ 变量|过滤器 }}, 如：使name的值标题化  {{ name|title }}
使用方式2：{% filter 过滤器 %} 变量 {% endfilter %}, 如：使name的值标题化  {% filter title %} name {% endfilter %}
还可以叠加使用：name|upper(转大写)|title(标题化)
常用的内置过滤器：length(长度)、escape(转义HTML文本)、safe(标记变量安全，避免转义)
http://jinja.pocoo.org/docs/2.10/templates/#builtin-filters   --完整的过滤器列表查看地址

自定义过滤器
在模板可以直接{{ text|musical }}进行使用
app.template_filter(name) 可以自定义名称 
如：@app.template_filter('check') 那么在模板就是{{ text|check }}进行使用
'''
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')  # Markup标记为安全，避免转义 同时在模板中使用 {{ text|safe }}也可以标记为安全
# 也可以这样添加自定义过滤器：app.jinja_env.filters["musical"] = musical
# 使用方式：{{ name|musical }}

'''
内置测试器(Jinja2提供)
http://jinja.pocoo.org/docs/2.10/templates/#list-of-builtin-tests   --完整的测试器列表查看地址

自定义测试器
在模板可以直接 {% if foo is baz() %} 或者 {% if foo is baz %} 进行使用
app.template_test(name) 可以自定义名称 
如：@app.template_filter('test') 
那么在模板就是 {% if foo is test() %} 或者 {% if foo is test %} 进行使用
'''
@app.template_test()
def baz(value):
    if value == 'baz':
        return True
    return False
# 也可以这样添加自定义测试器：app.jinja_env.tests["baz"] = baz

'''
模板环境对象：了解即可，不建议修改，容易出现兼容问题

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

'''
模板结构：
1、局部模板(局部模块的命名通常以一个下划线开始)：
{% include '_banner.html' %}

2、宏：
一般创建：macros.html 或者 _macros.htnm，内容实例：
{% macro qux(amount=1) %}
    {% if amount == 1 %}
        一个人
    {% elif amount > 1 %}
        多个人
    {% endif %}
{% endmacro %}
在其他模板使用：
先导入：{% form 'macros.htm' import qux %} 或者 {% form 'macros.htm' import qux with context %}
##
  with context是使得macros模板能使用
    自定义模板上下文处理器传入的变量、使用render_template()函数传入的变量、扩展使用内置的模板上下文处理函数提供的变量
  不写的话则无法使用
##
使用方式：{{ qux(amount=5) }}

3、模板继承：
模板：{% block content %}{% endblock content %}
继承：{% extends '主模板.html' %}  #必须是子模板的第一个标签
覆盖：同名的块，子模板会覆盖父模板的
追加:{% block 追加的块 %} {{ super() }} 追的内容 {% endblock 追加的块 %}
'''

'''
空白控制
<div>
{% if True -%}  #  -% 移除该语句后的空白
    <p>Hello!</p>
{%- endif %}    # %- 移除语句前的空白
</div>
也可以通过以下设置进行空白控制（注意宏内的空白控制不受这个影响）：
app.jinja_env.trim_blocks = True   #删除Jinja2语句后的第一个空行
app.jinja_env.lstrip_blocks = True #删除所在行之前的空格和制表符
'''

'''
消息闪现：flash()函数发送的消息会存储在session中
'''
@app.route('/flash')
def just_flash():
    flash('你好，我是闪电，欢迎登陆1')
    flash('你好，我是闪电，欢迎登陆2')
    return redirect(url_for('index'))

'''
自定义错误页面
app.errorhandler(错误状态码或者异常类)  如：@app.errorhandler(NameError)
当发生错误时，对应的错误处理函数就会被调用
参数e是异常类，该异常类的常用属性: code-错误码 name-原因短语 description-错误描述 （注意500的错误通常不会提供这几个属性，需要手动编写）
'''
# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', errorcode=e.code, errormsg=e.name, note=e.description), 404

# 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500