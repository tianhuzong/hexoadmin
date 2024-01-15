"""
作者:仙
email:tianhuzong@qq.com
Github : tianhuzong
Gitee: thzsen
bilibili:https://space.bilibili.com/349435428497240
"""
from flask import Flask ,render_template
from loguru import logger
from .utils import *
import subprocess
import os
app = Flask(__name__)


#Flask函数

@app.route("/")
def index():
    """
    主函数,打开网站
    """
    return render_template("index.html")

@app.route("page_list")
def page_list():
    """
    获取文章列表(返回一个字典)
    """
