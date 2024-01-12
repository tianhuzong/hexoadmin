from flask import Flask

import subprocess
import time
import os
app = Flask(__name__)

# function tools 一些函数工具
def gettime():
    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
def creat_page(path:str,title:str, tags:list, categories:list,date:str = gettime(),posts:bool = True):
    """
    创建一篇新的文章
    :param path hexo项目的根目录
    :param title 文章标题
    :param tags 文章标签的列表
    :param categories 文章分类的列表，列表后面的元素是前面的子分类
    :param date 创建文章的时间
    :param posts 是否为post，false则为草稿 
    """
    #生成标签的文本
    tags_text = "tags: "
    for x in tags:
        tags_text = tags_text + "\n- " + x 
    categories_text = "categories: "
    for y in categories:
        categories_text = categories_text + "\n- " + y
    content = f"""
---
title: {title}
date: {date}
{tags_text}
{categories_text}
---
    """
    if posts == True:
        post = "post"
    else : 
        post = "draft"
    os.chdir(path=path)
    subprocess.run(["hexo","new",post,title]) #生成hexo文章文件
    with open(path + r"/source/_" + post + "s/" + title + ".md",encoding="utf8",mode="w") as f :
        f.write(content)
def jiexitext(path):
    """
    解析一篇文章
    :param path 文章地址
    :return 返回一个字典
    """
    with open(path, mode="r", encoding="utf8") as f:
        text = f.readlines()
    
    # 解析文章头
    #print(text)
    del text[0]
    del text[0]
    #print(text,text[0],text[1])
    head = []
    for x in range(len(text)):
        if text[x] == "---\n":
            break
        else:
            head.append(text[x])
    
    # 解析正文
    body = "".join(text[x+1:])
    
    print(head)
    print("\n\n\n",body)
    