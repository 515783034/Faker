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
@LastEditTime: 2020-07-15 14:00:58
@FilePath: /faker/utils/file_utils.py
@Copyright: © 2020 Ashen23. All rights reserved.
'''

import os
import json
from flask import jsonify
from utils.readconfig import ReadConfig
from utils.log_utils import  logDebug, logError, logInfo

userConfig = ReadConfig()

jsonSubFix = ".json"

'''
@description: 读取url对应的文件内容
@param {url} 文件地址
@return: 文件内容
'''
def loadUrl(url):
    return _loadFile(jsonPathBy(url))

'''
@description: 从文件中加载序列化的json数据
'''
def loadJson(path):
    return jsonify(json.loads(_loadFile(path)))


# 写入文件
def writeJson(jsonPath, jsonContent):
    currentDir = os.path.dirname(jsonPath)
    if not os.path.exists(currentDir):
        os.makedirs(currentDir)
    with open(jsonPath, 'w', encoding="utf-8") as file:
        file.write(json.dumps(jsonContent, indent=4, ensure_ascii=False))

# 重命名json文件
def renameJson(name, newName, method):
    logDebug("[file]rename file: {} {}".format(name, newName))
    
    jsName = jsonPathBy(name)
    jsNewName = jsonPathBy(newName)
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
def deleteUrl(url):
    fileUrl = jsonPathBy(url)
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

'''
@description: 获取url对应的json文件路径
@param {url} url
@return: json文件路径
'''
def jsonPathBy(url):
    if not url.endswith(jsonSubFix):
        url += jsonSubFix
    if url.startswith("./jsons/"):
        return url
    return "./jsons/{}{}".format(userConfig.projectName(), url)

'''
@description: 从文件中加载数据
'''
def _loadFile(filepath):
    try:
        if not os.path.exists(filepath):
            logDebug("[file]-file not exist: {}".format(filepath))
            with open(userConfig.json("fileNotFound"), 'r', encoding="utf-8") as f:
                return f.read()
        with open(filepath, 'r', encoding="utf-8") as f:
            return f.read()
    except:
        return ""