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
@logger.catch
def index():
    """
    主函数,打开网站
    """
    if get_config()["code"] == 404: 
        return "<h1>请先运行/init进行初始化</h1>",404
    return "Hi"
    return render_template("index.html")
@app.route("/init",methods=["POST"])
@logger.catch
def init(): 
    """
    初始化函数，创建配置文件
    """
    #logger.info(request.json)
    sign = request.json.get("sign")
    data = request.json.get("data")
    logger.debug(json.dumps(data))
    path = data.get("path")
    APIkey = data.get("APIkey")
    if sign == None: 
        data = {"msg":"签名不存在"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey=")}) , 400
    if verify_sign(sign,json.dumps(data),APIkey) == False: 
        data = {"msg":"签名不合法"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey="+APIkey)}),400
    if os.path.exists(configpath := "./config.json") != True: 
        
        config = json.dumps({"path":path,"APIkey":APIkey})
        with open(configpath,mode="w",encoding="utf8") as f: 
            f.write(config)
        data = {"msg":"初始化成功"}
        return json.dumps({"code":200,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey="+APIkey)}),200
    else : 
        data = {"msg":"配置文件已存在"}
        return json.dumps({"code":403,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey="+APIkey)}),403
@app.route("/create_page",methods=["POST"])
@logger.catch
def createpage():
    """
    创建文章
    """
    configs = get_config()
    request_data = request.json
    if configs.get("code") == 404:
        data = {"msg":"配置文件不存在，请进行初始化"}
        return json.dumps({"code" : 404,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey=")}),404
    elif request_data.get("sign") == None : 
        data = {"msg":"签名不存在"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json,dumps(data))+"&APIkey=")}) , 400
    elif verify_sign(request_data.get("sign"),json.dumps(request_data.get("data")),configs["APIkey"]) == False: 
        logger.debug(f'{request_data.get("sign")},{json.dumps(request_data.get("data"))},{configs["APIkey"]}')
        data = {"msg":"签名不合法"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey="+configs["APIkey"])}),400

    post = request.json.get("data").get("post")
    title = request.json.get("data").get("title")
    if (date := request.json.get("data").get("date")) == None:
        date = gettime()
    tags = request.json.get("data").get("tags")
    categories = request.json.get("data").get("categories")
    content = request.json.get("data").get("content")
    

    if content == None: 
        content = ""
    res = create_page(configs["path"],title,tags,categories,date,post,content)
    if res == "Succeeded":
        data = {"msg":"文章创建成功"}
        return json.dumps({"code":200,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey=" + configs["APIkey"])}),200
    else: 
        data = {"msg":res}
        return json.dumps({"code":500,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey=" + configs["APIkey"])}),500
@app.route("/page_list/<int:page_size>/<int:page_number>",methods=["GET"])
@logger.catch
def get_page_list(page_size,page_number): 
    """
    获取文章列表
    """
    configs = get_config()
    logger.debug(request.view_args)
    request_data = request.view_args.copy()
    sign = request.args.get("sign")
    try:
        del request_data["sign"]
    except KeyError as e: 
        pass 
    if configs.get("code") == 404:
        data = {"msg":"配置文件不存在，请进行初始化"}
        return json.dumps({"code" : 404,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey=")}),404
    elif sign == None : 
        data = {"msg":"签名不存在"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey=")}) , 400
    elif verify_sign(sign,json.dumps(request_data),configs["APIkey"]) == False: 
        data = {"msg":"签名不合法"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey="+configs["APIkey"])}),400
    try: 
        plist , pages = page_list(configs["path"]+"/source",page_size,page_number)
    except Exception as e: 
        logger.error(f"捕获到一个错误：{e.args[0]}" )
        data = {"msg":e.args[0]}
        return json.dumps({"code":422,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey="+configs["APIkey"])}),422
    data = {"msg":"Sucessd!","list":plist,"page_nums":pages}
    return json.dumps({"code":200,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey=" + configs["APIkey"])}) , 200
@app.route("/page_list_a/<part>/<int:page_size>/<int:page_number>",methods=["GET"])
@logger.catch
def get_page_list_a(part,page_size,page_number): 
    """
    获取文章列表版本2
    """
    configs = get_config()
    logger.debug(request.view_args)
    request_data = request.view_args.copy()
    sign = request.args.get("sign")
    try:
        del request_data["sign"]
    except KeyError as e: 
        pass 
    if configs.get("code") == 404:
        data = {"msg":"配置文件不存在，请进行初始化"}
        return json.dumps({"code" : 404,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey=")}),404
    elif sign == None : 
        data = {"msg":"签名不存在"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey=")}) , 400
    elif verify_sign(sign,json.dumps(request_data),configs["APIkey"]) == False: 
        data = {"msg":"签名不合法"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey="+configs["APIkey"])}),400
    try: 
        plist , pages = page_list_a(configs["path"]+"/source",part,page_size,page_number)
    except Exception as e: 
        logger.error(f"捕获到一个错误：{e.args[0]}" )
        data = {"msg":e.args[0]}
        return json.dumps({"code":422,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey="+configs["APIkey"])}),422
    data = {"msg":"Sucessd!","list":plist,"page_nums":pages}
    return json.dumps({"code":200,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey=" + configs["APIkey"])}) , 200
@app.route("/update_head",methods=["PUT"])
@logger.catch
def update_head_view():
    """
    更新文章头部的函数
    """
    configs = get_config()
    request_data = request.json
    if configs.get("code") == 404:
        data = {"msg":"配置文件不存在，请进行初始化"}
        return json.dumps({"code" : 404,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey=")}),404
    elif request_data.get("sign") == None : 
        data = {"msg":"签名不存在"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json,dumps(data))+"&APIkey=")}) , 400
    elif verify_sign(request_data.get("sign"),json.dumps(request_data.get("data")),configs["APIkey"]) == False: 
        logger.debug(f'{request_data.get("sign")},{json.dumps(request_data.get("data"))},{configs["APIkey"]}')
        data = {"msg":"签名不合法"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey="+configs["APIkey"])}),400
    title = request.json.get("data").get("title")
    if (date := request.json.get("data").get("date")) == None:
        date = gettime()
    tags = request.json.get("data").get("tags")
    categories = request.json.get("data").get("categories")
    path = request.json.get("data").get("path")
    if os.path.exists(path) != True :
        data = {"msg":"文件不存在"}
        return json.dumps({"code":500,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey="+configs["APIkey"])}) , 500
    head_ls = jiexitext(path)[0]
    head_ls["tags"] = tags  
    head_ls["categories"] = categories 
    head_ls["date"] = date
    if (result := update_head(path,head_ls)) == "Succeeded":
        data = {"msg" : "头部更新成功"}
        return json.dumps({"code":200,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey="+configs["APIkey"])}) , 200
    else: 
        data = {"msg":result}
        return json.dumps({"code":500,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey="+configs["APIkey"])}) , 500
@app.route("/update_page",methods=["PUT"])
@logger.catch
def update_page_view():
    """
    更新文章头部的函数
    """
    configs = get_config()
    request_data = request.json
    if configs.get("code") == 404:
        data = {"msg":"配置文件不存在，请进行初始化"}
        return json.dumps({"code" : 404,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey=")}),404
    elif request_data.get("sign") == None : 
        data = {"msg":"签名不存在"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json,dumps(data))+"&APIkey=")}) , 400
    elif verify_sign(request_data.get("sign"),json.dumps(request_data.get("data")),configs["APIkey"]) == False: 
        logger.debug(f'{request_data.get("sign")},{json.dumps(request_data.get("data"))},{configs["APIkey"]}')
        data = {"msg":"签名不合法"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey="+configs["APIkey"])}),400
    content = request_data.get("content")
    path = request.json.get("data").get("path")
    if os.path.exists(path) != True :
        data = {"msg":"文件不存在"}
        return json.dumps({"code":500,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey="+configs["APIkey"])}) , 500
    if (result := update_page(path,content)) == "Succeeded":
        data = {"msg" : "文章内容更新成功更新成功"}
        return json.dumps({"code":200,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey="+configs["APIkey"])}) , 200
    else: 
        data = {"msg":result}
        return json.dumps({"code":500,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey="+configs["APIkey"])}) , 500
@app.route("/tags_list/<int:page_size>/<int:page_num>",methods=["GET"])
@logger.catch
def tag_list(page_size,page_num):
    """
    获取标签列表
    """
    configs = get_config()
    logger.debug(request.view_args)
    request_data = request.view_args.copy()
    sign = request.args.get("sign")
    try:
        del request_data["sign"]
    except KeyError as e: 
        pass 
    if configs.get("code") == 404:
        data = {"msg":"配置文件不存在，请进行初始化"}
        return json.dumps({"code" : 404,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey=")}),404
    elif sign == None : 
        data = {"msg":"签名不存在"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json.dumps(data))+"&APIkey=")}) , 400
    elif verify_sign(sign,json.dumps(request_data),configs["APIkey"]) == False: 
        data = {"msg":"签名不合法"}
        return json.dumps({"code":400,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey="+configs["APIkey"])}),400
    try: 
        tagslist , tags = get_tags_list(page_size,page_num)
    except Exception as e: 
        logger.error(f"捕获到一个错误：{e.args[0]}" )
        data = {"msg":e.args[0]}
        return json.dumps({"code":422,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey="+configs["APIkey"])}),422
    data = {"msg":"Sucessd!","list":tagslist,"page_nums":tags}
    return json.dumps({"code":200,"data":data,"sign":md5(json2pathValue(json.dumps(data)) + "&APIkey=" + configs["APIkey"])}) , 200
if __name__ == "__main__":
    logger.add("logs/{time:YYYY-MM-DD}.log",encoding="utf8",enqueue=True,rotation="00:00",level="DEBUG")
    app.run(host="0.0.0.0",port="5000")