"""
作者:仙
email:tianhuzong@qq.com
Github : tianhuzong
Gitee: thzsen
bilibili:https://space.bilibili.com/349435428497240
"""
from flask import Flask ,render_template ,request
from loguru import logger
from utils import *
import subprocess
import os
app = Flask(__name__)



#Flask函数

@app.route("/")
def index():
    """
    主函数,打开网站
    """
    return "Hi"
    return render_template("index.html")
@app.route("/init",methods=["POST"])
def init(): 
    """
    初始化函数，创建配置文件
    """
    if os.path.exists(configpath := "./config.json") != True: 
        path = request.form.get("path")
        config = json.dumps({"path":path})
        with open(configpath,mode="w",encoding="utf8") as f: 
            f.write(config)
        return json.dumps({"code":200,"msg":"初始化成功"})
    else : return json.dumps({"code":403,"msg":"配置文件已存在"})
@app.route("/create_page",methods=["POST"])
def createpage():
    """
    创建文章
    """
    post = request.form.get("post")
    title = request.form.get("title")
    if (date := request.form.get("date")) == None:
        date = gettime()
    logger.debug(request.method)
    logger.debug(request.form)
    tags = request.form.get("tags")
    logger.debug(tags)
    categories = request.form.get("categories")
    logger.debug(categories)
    content = request.form.get("content")
    configs = get_config()
    # TODO 把下面接口复原 
    """
    if configs["code"] == 404:
        return json.dumps({"code" : 404,"msg":"配置文件不存在，请进行初始化"})
    """
    # TODO 把下面这一行删掉
    
    configs["path"] = "/workspace/cloud-studio-python-demo/testcli"
    if content == None: 
        content = ""
    res = create_page(configs["path"],title,tags,categories,date,post,content)
    if res == "Successd":
        return json.dumps({"code":200,"msg":"文章创建成功"})
    else: return json.dumps({"code":500,"msg":res})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port="5000")