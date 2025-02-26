import click
from flask import Flask

__author__ = "zhangjh"

app = Flask(__name__)
# 项目配置名称必须全部大写
app.config["ADMIN_NAME"] = "zhangjh"

# 项目配置多个
app.config.update(
    TESTING=True,
    SECRET_KEY="sdjfsdg98723"
)
# 读取项目配置
value = app.config["ADMIN_NAME"]

@app.route('/')
def index():
    return '<h1>Hello Flask!</h1>'

@app.route('/hi')
@app.route('/hello')
def sqy_hello():
    return '<h1>Hi Flask!</h1>'

@app.route('/greet', defaults={'name': '游客'})
@app.route('/greet/<name>')
def greet(name):
    return f'<h1>Hello {name}!</h1>'

'''
Flask命令：
  flask --help  查看帮助文档
  flask routes  显示所有注册的路由.
  flask run     启动flask.
  flask shell   打开flask交互式解释器.
'''
@app.cli.command()
def hello():
    """
    通过创建任意一个函数，并为其添加app.cli.command()装饰器，我们就可以注册一个flask命令
    函数名称即为命令名称：如以下的命令为 flask hello
    也可以在app.cli.command()传入参数来设置命令名称，比如：app.cli.command('say-hello')，命令就变为flask say-hello
    """
    click.echo("Hello, everyone!")