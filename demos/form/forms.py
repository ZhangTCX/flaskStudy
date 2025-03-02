# -*- coding : utf-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, MultipleFileField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email
from flask_ckeditor import CKEditorField

"""
常用的 WTForms 字段
字段类                |            对应的 HTML 表示                           |                   说明                              
-----------------------------------------------------------------------------------------------------------------------
BooleanField         |       <input type="checkbox">                       |    复选框,值会被处理为True或False                 
DateField            |       <input type="text">                           |    文本字段,值会被处理为datetime.date对象         
DateTimeField        |       <input type="text">                           |    文本字段,值会被处理为 datetime.datetime对象    
FileField            |       <input type-"file">                           |    文件上传字段                                   
FloatField           |       <input type="text">                           |    浮点数字段,值会被处理为浮点型                  
IntegerField         |       <input type="text">                           |    整数字段,值会被处理为整型                      
RadioField           |       <input type="radio">                          |    一组单选按钮                                   
SelectField          |       <select><option></option></select>            |    下拉列表                                       
SelectMultipleField  |       <select multiple><option></option></select>   |    多选下拉列表                                   
SubmitField          |       <input type="submit">                         |    提交按钮                                       
StringField          |       <input type="text">                           |    文本字段                                       
HiddenField          |       <input type="hidden">                         |    隐藏文本字段                                   
PasswordField        |       <input type="password">                       |    密码文本字段                                   
TextAreaField        |       <textarea></textarea>                         |    多行文本字段                                   
"""

# 表单类
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField("Remember me")
    submit = SubmitField('Login')
    """
    --实例化字段类常用参数
    label      | 字段标签<label>的值，也就是渲染后显示在输入字段前的文字
    render_kw  | 一个字典，用来设置对应的HTML<input标签的属性，比如传入{"placeholder":"YourName"}，
                 渲染后的HTML代码会将<input>标签的placeholder属性设为Your Name
    validators | 一个列表，包含一系列验证器，会在表单提交后被逐一调用验证表单数据
    default    | 字符串或可调用对象，用来为表单字段设置默认值

    --常用的WTForms验证器
    DataRequired(message=None)                          | 验证数据是否有效
    Email(message=None)                                 | 验证Email地址
    EqualTo(fieldname, message=None)                    | 验证两个字段值是否相同
    InputRequired(message=None)                         | 验证是否有数据
    Length(min=-1, max=-1, message=None)                | 验证输入值长度是否在给定范围内
    NumberRange(min=None, max=None, message=None)       | 验证输入数字是否在给定范围内
    Optional(strip_whitespace=True)                     | 允许输入值为空，并跳过其他验证
    Regexp(regex, flags=0, message=None)                | 使用正则表达式验证输人值
    URL(require_tld=True, message=None)                 | 验证URL
    AnyÓf(values, message=None, values_formatter=None)  | 确保输入值在可选值列表中
    NoneOf(values, message=None, values_formatter=None) | 确保输入值不在可选值列表中
    (在实例化验证类时，message参数用来传入自定义错误消息,如:DataRequired(message="用户名不能为空")，如果没有设置则使用内置的英文错误消息，
    后面我们会了解如何使用内置的中文错误消息)
    """

    """
    默认情况下，WTForms输出的字段HTML代码只会包含id和name属性，属性值均为表单类中对应的字段属性名称。如果要添加额外的属性，通常有两种方法。
    方法1：使用 render_kw 属性
    username = StringField('Username', render_kw={'placeholder':'Your Username'))
    输出HTML结果
    <input type="text" id="username" name="username" placeholder="Your Username">
    
    方法2: 在调用字段时传入
    form.username(style='width:200px;',class_ ='bar')  注意:class是Python的保留关键字，在这里我们使用class_来代替class
    输出HTML结果
    <input class="bar" id="username" name="username" style="width:200px;" type="text">'
    
    Tips:通过上面的方法也可以修改id和name属性，但表单被提交后，WTForms需要通过name属性来获取对应的数据，所以不能修改name属性值。
    """

"""
自定义验证器(2种)
"""
# 第一种：行内验证器(不建议使用)
class FortyTwoFormOut(FlaskForm):
    answer = IntegerField('The Number')
    submit = SubmitField('Submit')
    # 当表单类中包含以“validate_属性名”形式命名的方法时，再验证字段数据时会同同时调用这个方法来验证对应的字段
    # 所以表单类的字段属性名不能以validate开头，这种方法仅用来验证特定的表单类字段，所以称为行内验证器
    def validate_answer(form, field):
        if field.data != 42:
            raise ValidationError("Must be 42.")

# 第二种：全局验证器
'''
# 1.无参写法
def is_42(form, field):
    if field.data != 42:
        raise ValidationError("Must be 42.")
class FortyTwoForm(FlaskForm):
    answer = IntegerField('The Number', validators=[is_42])
    submit = SubmitField('Submit')
'''
# 2.有参写法
def is_42(message=None):
    if message is None:
        message = "Must be 42."
    def _is_42(form, field):
        if field.data != 42:
            raise ValidationError(message)
    return _is_42

class FortyTwoForm(FlaskForm):
    answer = IntegerField('The Number', validators=[is_42()])
    submit = SubmitField('Submit')


"""
文件上传
"""
class UploadForm(FlaskForm):
    # 文件相关验证器
    # 1.FileRequired(message=None)  验证是否包含文件对象
    # 2.FileAllowed(upload_set, message=None)  用来验证文件类型，upload_set参数用来传入包含允许的文件后缀名列表
    # Tips: 客户端的验证可以使用HTML5中的accept属性实现简单的过滤，如<input type='file' accept=".jpg, .jpeg, .png, .gif">
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('Submit')

"""
多文件上传
"""
class MultiFileForm(FlaskForm):
    photo = MultipleFileField('Upload Image', validators=[DataRequired()])
    submit = SubmitField('Submit')

"""
富文本编辑器：flask_ckeditor
      配置键              默认值                 说明
CKEDITOR_SERVE_LOCAL     False        设为True会使用内置的本地资源
CKEDITOR_PKG_TYPE      'standard'     CKEditor包类型，可选值为basic(基础功能包)、standard(标准功能包)和full(完整功能包) 
CKEDITOR_LANGUAGE          ''         界面语言，传入ISO639格式的语言码
CKEDITOR_HEIGHT            ''         编辑器高度
CKEDITOR_WIDTH             ''         编辑器宽度
配置方式：app.config['CKEDITOR_SERVE_LOCAL'] = True
"""
class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Publish')

# 单个表单多个提交按钮
class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = TextAreaField('Body', validators=[DataRequired()])
    save = SubmitField('Save') # 保存草稿箱按钮
    publish = SubmitField('Publish') # 发布按钮

# 单个页面多个表单

# 单视图处理(两个表单的提交字段设置不同的名称)
class SigninForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit1 = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit2 = SubmitField('Register')

# 多视图处理(提交字段可以一致)
class SigninForm2(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit = SubmitField('Sign in')

class RegisterForm2(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit = SubmitField('Register')