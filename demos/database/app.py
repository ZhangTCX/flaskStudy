# -*- coding : utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__author__ = "zhangjh"

app = Flask(__name__)

db = SQLAlchemy(app)