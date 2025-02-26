# -*- coding : utf-8 -*-
import os
from flask import Flask
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

__author__ = "zhangjh"

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
class LoginForm(Form):
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
    (在实例化验证类时，message参数用来传入自定义错误消息，如果没有设置则使用内置的英文错误消息，后面我们会了解如何使用内置的中文错误消息)
    """
    username = StringField('Username', validators=[DataRequired(message="用户名不能为空")])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField("Remember me")
    submit = SubmitField('Login')






app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'secret string')


