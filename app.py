from flask import Flask
from loguru import logger
import subprocess
import time
import os
app = Flask(__name__)

# function tools 一些函数工具
def gettime():
    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
def get_middle_text(text, start_marker, end_marker):
    """
    取出文本中间
    :param text 原文本
    :param start_maker 文本开始 
    :param end_maker 文本结束
    :return 返回中间文本
    """
    start_index = text.find(start_marker) + len(start_marker)
    end_index = text.find(end_marker)
    
    middle_text = text[start_index:end_index]
    return middle_text.lstrip()
def creat_page(path:str,title:str, tags:list, categories:list,date:str = gettime(),posts:bool = True,text_content:str = ""):
    """
    创建一篇新的文章
    :param path hexo项目的根目录
    :param title 文章标题
    :param tags 文章标签的列表
    :param categories 文章分类的列表，列表后面的元素是前面的子分类
    :param date 创建文章的时间
    :param posts 是否为post，false则为草稿
    :param text_content 文章正文，默认为空 
    """
    #生成标签的文本
    tags_text = "tags: "
    for x in tags:
        tags_text = tags_text + "\n- " + x 
    categories_text = "categories: ["
    for y in categories:
        categories_text = categories_text + y + ","
    categories_text += "]"
    content = f"""---
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
        f.write(content + text_content)
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
    
    jiexires : dict = {}

    #解析头部信息
    for x in range(len(head)):
        index = get_middle_text(head[x],"",":")
        #logger.debug(index)
        if index == "tags":
            tagslist = []
            head_x1 = head[x+1 :]
            for y in range(len(head_x1)):
                #logger.debug(f"{y},{head_x1[y]}")
                if head_x1[y][0:2] == "- ":
                    #logger.debug(head_x1[y])
                    tagslist.append(n := (get_middle_text(head_x1[y],"- ","\n")).rstrip())
                    #logger.debug(n)
            addtext = "[\"" + "\",".join(tagslist)
            jiexires[index] = addtext + "\"]"
            continue
        elif index[0:2] == "- ":
            continue
        elif index == "categories":
            cats = get_middle_text(get_middle_text(head[x],": ","\n"),"[","]").split(",")
            logger.debug(cats)
            addtext = "[" + ",".join(cats) + "]"
            jiexires[index] = addtext
            continue
        jiexires[index] = get_middle_text(head[x],":","\n")
    jiexires["body"] = body
    return jiexires
    