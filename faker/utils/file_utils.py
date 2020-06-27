'''
                       .::::.
                     .::::::::.
                    :::::::::::
                 ..:::::::::::'
              '::::::::::::'
                .::::::::::
           '::::::::::::::..
                ..::::::::::::.
              ``::::::::::::::::
               ::::``:::::::::'        .:::.
              ::::'   ':::::'       .::::::::.
            .::::'      ::::     .:::::::'::::.
           .:::'       :::::  .:::::::::' ':::::.
          .::'        :::::.:::::::::'      ':::::.
         .::'         ::::::::::::::'         ``::::.
     ...:::           ::::::::::::'              ``::.
    ````':.          ':::::::::'                  ::::..
                       '.:::::'                    ':'````..

@Description: 文件相关处理
@Author: ashen23
@LastEditTime: 2020-06-24 13:46:48
@FilePath: /faker/faker/utils/file_utils.py
@Copyright: © 2020 Ashen23. All rights reserved.
'''

import os
import json
from flask import jsonify
from utils.readconfig import ReadConfig
from utils.log_utils import  logDebug, logError, logInfo

userConfig = ReadConfig()

'''
@description: 读取url对应的文件内容
@param {url} 文件地址
@return: 文件内容
'''
def loadUrl(url, method):
    try:
        fileUrl = jsonPathBy(url, method)
        if not os.path.exists(fileUrl):
            logDebug("[file]file not exist: {}".format(fileUrl))
            return loadFile(userConfig.json("fileNotFound"))
        with open(fileUrl, 'r', encoding="utf-8") as f:
            return f.read()
    except:
        return ""

'''
@description: 从文件中加载数据
'''
def loadFile(path):
    try:
        if not os.path.exists(path):
            logDebug("[file]-file not exist: {}".format(path))
            with open(userConfig.json("fileNotFound"), 'r', encoding="utf-8") as f:
                return f.read()
        with open(path, 'r', encoding="utf-8") as f:
            return f.read()
    except:
        return ""

'''
@description: 从文件中加载json数据
'''
def loadJson(path):
    return jsonify(json.loads(loadFile(path)))


# 写入文件
def writeJson(name, json_content):
    new_dir = os.path.dirname(name)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    with open(name, 'w', encoding="utf-8") as file:
        file.write(json.dumps(json_content, indent=4, ensure_ascii=False))

# 重命名json文件
def renameJson(name,newName, method):
    logDebug("[file]rename file: {} {}".format(name, newName))
    
    jsName = jsonPathBy(name, method)
    jsNewName = jsonPathBy(newName, method)
    if not os.path.exists(jsName):
        logDebug("[file] rename not exist: {}".format(name))
        return
    new_dir = os.path.dirname(jsNewName)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    
    os.rename(jsName, jsNewName)

'''
@description: 根据url删除对应的json文件
'''
def deleteUrl(url, method):
    fileUrl = jsonPathBy(url, method)
    if os.path.exists(fileUrl):
        logDebug("[file]delete url: {}".format(fileUrl))
        os.remove(fileUrl)

'''
@description: 获取地址的文件吗
@param {type} 文件地址
@return: 文件名(a.txt)
'''
def nameBy(url):
    return url.split("/")[-1]

def allNameBy(url, method):
    return "({}){}".format(method, nameBy(url))

'''
@description: 获取url的路径(除文件名)
@param {type} 
@return: 
'''
def pathBy(url):
    return os.path.dirname(url) + "/"

'''
@description: 获取url对应的json文件路径
@param {url} url
@return: json文件路径
'''
def jsonPathBy(url, method):
    newUrl = pathBy(url) + allNameBy(url, method)
    return "./jsons/{}{}".format(userConfig.projectName(), newUrl)