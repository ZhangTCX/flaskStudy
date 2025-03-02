# -*- coding : utf-8 -*-
import os
import uuid

from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory
from werkzeug.datastructures import FileStorage

from forms import (LoginForm, FortyTwoForm, UploadForm, MultiFileForm, RichTextForm, NewPostForm, SigninForm,
                   RegisterForm, SigninForm2, RegisterForm2)
from werkzeug.utils import secure_filename
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from flask_ckeditor import CKEditor

__author__ = "zhangjh"

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'secret string')
# 设置请求报文最大长度(单位:字节(byte))
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024  # 限制3M
# 设置文件上传路径
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
# 允许上传图片的后缀
app.config['AllOWED_EXTENSIONS'] = ['jpg', 'jpeg', 'png', 'gif']
# 使用内置的本地资源(富文本编辑器) （需下载CKEditor）
app.config['CKEDITOR_SERVE_LOCAL'] = True

ckeditor = CKEditor(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    # if request.method == 'POST' and form.validate():
    # Flask-WTF提供了validate_on_submit()方法合并了这2个操作(除了POST,请求方法是PUT、PATCH和DELETE方法也会验证)
    if form.validate_on_submit():
        # 处理POST请求
        username =  form.username.data
        flash(f"Welcome home, {username}!")
        return redirect(url_for('index'))  # 重定向响应，防止重复提交表单(PRG模式-不让POST请求作为最后一个请求)
    # 处理GET请求
    return render_template('basic.html', form=form)

@app.route('/bootstrap', methods=['GET', 'POST'])
def bootstrap():
    form = LoginForm()
    if form.validate_on_submit():
        # 处理POST请求
        username = form.username.data
        flash(f"Welcome home, {username}!")
        return redirect(url_for('index'))
    return render_template('bootstrap.html', form=form)

"""
1.提交表单
    HTML表单中控制提交行为的属性
    action:
        默认值：当前URL，即页面对应的URL 
        说明：表单提交时发送请求目标的URL
    method:
        默认值：get 
        说明：提交表单的HTTP请求方法，目前仅支持使用GET和POST方法
    enctype: 
        默认值：application/x-www-form-urlencoded 
        说明：表单数据的编码类型，当表单中包含文件上传字段时，需要设为multipart/form-data,还可以设为纯文本类型text/plain
2.验证表单数据
    1.客户端验证
        比如：添加 required 标志 - 用户没有输入内容而按下提交按钮会弹出内置的错误提示, 如：{{ form.username(required='') }}
        除了使用HTML5提供的属性实现基本的客户端验证，我们通常会使用JavaScript实现完善的验证机制。
        JavaScript表单验证库,比如
        jQuery Validation Plugin( https://jqueryvalidation.org/)
        Parsleyjs(http://parsleyis.org/)
        Bootstrap Validator ( http://1000hz.github.io/bootstrap-validator/，目前仅支持 Bootstrap3 版本)。
    2.服务器端验证(重点)
        验证方法-validate()介绍: 
            form = LoginForm(username='', password='123')
            >>> form.data
            {'username':'', 'password':'123'}
            >>> form.validate()
            False
            >>> form.errors
            {'username':'This field is required.', 'password':'Field must be between 8 and 128 characters long.'} 
            
        验证器DataRequired和InputRequired验证器会自动添加required属性,
        同时还会添加form.username.flags.required标志,我们可以通过这个标志值来判断标志文本为必输 
"""

"""
使用宏渲染表单操作(减少大量重复代码): 查看 macros.html 和 basic_macros.html
"""
@app.route('/basic_macros', methods=['GET', 'POST'])
def basic_macros():
    form = LoginForm()
    return render_template('basic_macros.html', form=form)

"""
自定义验证器
"""
@app.route('/forty_two_form', methods=['GET', 'POST'])
def forty_two_form():
    form = FortyTwoForm()
    return render_template('forty_two_form.html', form=form)

"""
文件上传
    验证文件类型
    验证文件大小
    过滤文件名
"""
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print(app.root_path)
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data # <FileStorage: '图片名.jpg' ('image/jpeg')>
        # 过滤文件名方案1：原文件名(确认安全的情况下使用)
        # filename = f.filename

        # 过滤文件名方案2：werkzeug提供的secure_filename()会过滤掉文件名中的非ASCII字符，
        #               但如果文件名完全由非ASCII字符组成，就得到的是一个空文件名了
        # filename = secure_filename(f.filename)

        # 过滤文件名方案3：对上传的文件重新命名，使用Python内置的uuid模块生成随机文件名(安全)
        filename = random_filename(f.filename)

        # 保存图片
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Uploaded success.')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))

    return render_template('upload.html', form=form)

@app.route('/upload/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')

def random_filename(filename) -> str:
    """
    使用Python内置的uuid模块生成随机文件名
    :param filename: 原文件名
    :return: 随机新文件名
    """
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

@app.route('/upload-images', methods=['GET', 'POST'])
def multi_upload():
    form = MultiFileForm()
    if form.validate_on_submit():
        filenames = []
        # 验证CSRF令牌
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError as e:
            flash("CSRF token error: %s" % e)
            return redirect(url_for('multi_upload'))
        # 检查文件是否存在
        # 确保字段中包含文件数据(相当于FileRequired验证器)，如果用户没有选择文件就提交表单则request.files将为空
        if 'photo' not in request.files:
            flash('This field is required.')
            return redirect(url_for('multi_upload'))
        # 对request.files属性调用getlist()方法并传入字段的name属性值会返回包含所有上传文件对象列表
        for f in request.files.getlist('photo'):
            # 检查文件类型
            if isinstance(f, FileStorage) and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                filenames.append(filename)
            else:
                flash('Invalid file type.')
                return redirect(url_for('multi_upload'))
        flash('Uploaded success.')
        session['filenames'] = filenames
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['AllOWED_EXTENSIONS']

@app.route('/ckeditor', methods=['GET', 'POST'])
def integrate_ckeditor():
    form = RichTextForm()
    return render_template('ckeditor.html', form=form)

@app.route('/two-submits', methods=['GET', 'POST'])
def two_submits():
    form = NewPostForm()
    if form.validate_on_submit():
        '''
        对于单击提交字段的值，会将其转换为布尔值
        被单击的提交字段的值将是True，未被单击的值则是False
        '''
        if form.save.data:  # 保存按钮被点击
            # 保存草稿箱
            flash('You click the "Save" button.')
        elif form.publish.data:
            # 发布按钮
            flash('You click the "Publish" button.')
        return redirect(url_for('index'))
    return render_template("2submit.html",form=form)

@app.route('/multi-form', methods=['GET', 'POST'])
def multi_form():
    signin_form = SigninForm()
    register_form = RegisterForm()

    if signin_form.submit1.data and signin_form.validate():
        username = signin_form.username.data
        flash(f'{username}, you just submit the Signin Form.')
        return redirect(url_for('index'))

    if register_form.submit2.data and register_form.validate():
        username = register_form.username.data
        flash(f'{username}, you just submit the Register Form.')
        return redirect(url_for('index'))

    return render_template('2form.html', signin_form=signin_form, register_form=register_form)

@app.route('/multi-form-multi-view')
def multi_from_multi_view():
    signin_form = SigninForm2()
    register_form = RegisterForm2()
    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)

@app.route('/handle_signin', methods=['POST'])
def handle_signin():
    signin_form = SigninForm2()
    register_form = RegisterForm2()
    if signin_form.validate_on_submit():
        username = signin_form.username.data
        flash(f'{username}, you just submit the Signin Form.')
        return redirect(url_for('index'))
    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)

@app.route('/handle_register', methods=['POST'])
def handle_register():
    signin_form = SigninForm2()
    register_form = RegisterForm2()
    if register_form.validate_on_submit():
        username = register_form.username.data
        flash(f'{username}, you just submit the Register Form.')
        return redirect(url_for('index'))
    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)
