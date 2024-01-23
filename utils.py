"""
作者:仙
email:tianhuzong@qq.com
Github : tianhuzong
Gitee: thzsen
bilibili:https://space.bilibili.com/349435428497240
"""
from loguru import logger
import subprocess
import datetime
import os
import yaml
import json
import re
import hashlib
def gettime():
    return  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
def create_page(path:str,title:str, tags:list, categories:list,date:str = gettime(),posts :str = "post",text_content:str = ""):
    """
    创建一篇新的文章
    :param path hexo项目的根目录
    :param title 文章标题
    :param tags 文章标签的列表
    :param categories 文章分类的列表，列表后面的元素是前面的子分类
    :param date 创建文章的时间
    :param posts 文件布局,默认为post.选项如下:post,draft,page。post为发布的文章,draft为草稿,page为页面(例如关于页,友链页) 
    :param text_content 文章正文，默认为空 
    """
    #生成标签的文本
    tags_text = "tags: "
    for x in tags:
        tags_text = tags_text + "\n- " + x 
    categories_text = "categories: ["
    for y in categories:
        categories_text = categories_text + f"{y}" + ","
    categories_text += "]"
    
    content = f"""---
title: {title}
date: {date}
{tags_text}
{categories_text}
---
"""

    logger.debug(text_content)
    #os.chdir(path=path)
    if posts in ["post","draft"]:
        if (os.path.exists(path + r"/source/_posts/" + title + ".md") == True) or (os.path.exists(path + "/source/_drafts/" + title + ".md") == True):
            return "文件已存在"
        else: 
            #workpath = os.getcwd()
            #os.chdir(path)
            stdoutput = subprocess.Popen(f"cd {path} && hexo new {posts} {title}",stdout=subprocess.PIPE,shell=True).communicate()[0] #生成hexo文章文件            
            #os.chdir(workpath)
            try:
                with open((path + r"/source/_" + posts + "s/" + title + ".md"),encoding="utf8",mode="w") as f :
                    f.write(content + text_content)
            except Exception as e: 
                logger.error(e)
                os.remove(n)
                return "文件创建失败，原因：" + e.args[0]
    elif posts == "page":
        """对页面进行查重"""
        if os.path.exists(path + "/source/" + title) == True : 
            return "页面已存在"
        else: 
            #workpath = os.getcwd()
            #os.chdir(path)
            stdoutput = subprocess.Popen(f"cd {path} && hexo new {posts} {title}",stdout=subprocess.PIPE,shell=True).communicate()[0] #生成hexo文章文件
            #os.chdir(workpath)
            try:
                with open((path + r"/source/" +  title + "/index.md"),encoding="utf8",mode="w") as f :
                    f.write(content + text_content)
            except Exception as e: 
                logger.error(e)
                os.remove(n)
                return "文件创建失败，原因：" + e.args[0]
    if "INFO  Validating config\nINFO  Created:" in stdoutput.decode():
        return "Successd"

#废弃
def jiexi_request(tags,categories):
    """
    解析请求体，由于模块请求的特殊，需要解析
    """ 
    tags_list = re.findall(r"'([^']*)'", tags, flags=0)
    if len(tags_list) == 0: 
        tags_list = tags.split(",")
    categories_list = re.findall(r"'([^']*)'", categories, flags=0)
    if len(categories_list) == 0:
        categories_list = categories.split(",")
    return tags_list,categories_list
def jiexitext_myself(path):
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



"""
版权声明：本文为CSDN博主「xiejava1018」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/fullbug/article/details/126007706
"""

def jiexitext(blog_md_file) -> tuple:
    #读md文件
    md_f = open(blog_md_file, "r",encoding='utf-8')
    md_f_str=md_f.read()
    #解析两个---之间的内容
    pattern='---'
    blog_data={}
    pattern_list=list(pattern_search(md_f_str, pattern))
    if len(pattern_list)>=2:
        blog_info_str=md_f_str[pattern_list[0]+len(pattern):pattern_list[1]]
        blog_data=yaml.load(blog_info_str,Loader=yaml.SafeLoader)
        
        content = md_f_str[pattern_list[1]+len(pattern):]
    md_f.close()
    return blog_data,content


def pattern_search(string,pattern):
    '''分割符号匹配检索'''
    index=0
    while index<len(string)-len(pattern):
        index=string.find(pattern,index,len(string))
        if index==-1:
            break
        yield index
        index+=len(pattern)-1

def dict_to_md(blog_data, content):
    # 获取原始 Markdown 内容  
    original_md_content = content
    blog = dict(blog_data)
    #logger.debug(f"{type(blog['date'])},{type(blog_data['date'])},{blog is blog_data}")
    # 将 date 字段的值转换为特定格式的字符串
    if ('date' in blog) and (type(blog['date']) == type(datetime.datetime)):
        blog['date'] = blog['date'].strftime('%Y-%m-%d %H:%M:%S')

    # 将 YAML 数据重新转换为字符串  
    yaml_str = yaml.dump(blog, default_flow_style=False, allow_unicode=True)
      
    # 合并原始 Markdown 内容和转换后的 YAML 字符串，并在它们之间插入两个“---”  
    reversed_content = f'---\n{yaml_str}\n---\n{original_md_content}'
    return reversed_content


def update_page(path,text_content):
    """
    更新文章内容，不需要编写文章头部内容
    :param path 文章目录
    :param text_content
    """
    jiexi = jiexitext(path)
    #logger.debug(f"{jiexi} {jiexi[0]} {type(jiexi[0]['date'])}")
    text = dict_to_md(jiexi[0],text_content)
    if os.path.exists(path) != True:
        return "文件不存在"
    with open(path,mode="w+",encoding="utf8") as f:
        f.write(text)
    return "Successd"
def update_head(path,head : dict):
    """
    更新文章头部的yaml配置
    :param path 文件路径
    :param head 头部,字典
    """
    if os.path.exists(path) != True:
        return "文件不存在"
    text_jiexi = jiexitext(path)
    res = dict_to_md(head,jiexitext[1])
    with open(path,mode="w",encoding="utf8") as f:
        f.write(res)
    return "Sucess"

def page_list(path,page_size,page_number): 
    """
    获取文章列表
    :param path source目录的绝对路径
    :type str
    :param page_size
    :return 返回文章的列表
    :type list
    """
    file_list = []
    
    # 遍历目录中的所有文件和文件夹
    for root, dirs, files in os.walk(path):
        # 遍历当前目录中的文件
        for file_name in files:
            # 将文件的完整路径加入到列表中
            file_list.append(os.path.join(root, file_name))
    
    # 计算文件列表的总页数
    total_pages = (len(file_list) + page_size - 1) // page_size
    
    # 验证页码是否超过最大页数
    if page_number > total_pages:
        raise ValueError("获取的页码已经超过最大页数")
    
    # 根据指定的页码和每页数量计算分页范围
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    
    # 对文件列表进行分页处理
    paginated_list = file_list[start_index:end_index]
    
    return paginated_list, total_pages

def get_tags_list(page_size):
    """
    获取标签列表
    :param page_size
    :type int
    :param page_num 获取第几页
    :return 返回一个列表和总页数
    """

def get_config():
    if os.path.exists("./config.json") != True: 
        return {"code":404}
    with open("./config.json",mode="r",encoding="utf8") as f: 
        configs = json.loads(f.read())
        configs["code"] = 200
    return configs
def json2pathValue(json_object):
    json_dict = json.loads(json_object)
    key_list = sorted(list(json_dict.keys()))
    result = []
    for key in key_list:
        value = json_dict[key]
        if value is None or value == "":
            result.append(f"{key}=")
        else:
            result.append(f"{key}={value}")
    return "&".join(result).replace("'",'"').replace(" ","")
def md5(str):
    return hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()
def verify_sign(sign,data,APIkey):
    """
    sign签名验证
    :param sign sign的签名
    :param data 被签名的数据,json字符串,不包含APIkey
    :param APIkey 
    :return bool,签名合法为True,不合法为False
    """
    sign_1 = md5(json2pathValue(data)+"&APIkey="+APIkey) #本地计算的sign签名
    if sign_1 == sign: 
        return True
    else : return False