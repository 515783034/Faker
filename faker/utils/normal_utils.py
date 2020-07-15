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

@Description: 处理 api.ini 配置
@Author: ashen23
@LastEditTime: 2020-07-14 11:04:21
@FilePath: /faker/utils/normal_utils.py
@Copyright: © 2020 Ashen23. All rights reserved.
'''

import json
import socket
from flask import jsonify
from utils.file_utils import loadJson
from utils.log_utils import  logDebug, logError, logInfo
from utils.readconfig import ReadConfig
userConfig = ReadConfig()

# 获取本机ip地址
def getLocalIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return 'http://' + ip + ':5000/'


def resSuccess(res=None):
    return jsonify({'code':1, 'msg':'成功', 'data': res})

def resNotFound():
    return loadJson(userConfig.json("apiNotFound"))

def resError(error):
    logError(error)
    return jsonify({'code':-1,'msg':error})


# 可选的分组图标
def groupIcons():
    icons = ["el-icon-s-tools", "el-icon-setting", "el-icon-user", "el-icon-phone-outline", "el-icon-more-outline", "el-icon-star-off","el-icon-goods",
    "el-icon-warning-outline", "el-icon-info","el-icon-help", "el-icon-s-help","el-icon-picture-outline",
    "el-icon-picture-outline-round", "el-icon-upload", "el-icon-video-camera","el-icon-s-platform","el-icon-s-promotion",
    "el-icon-s-flag","el-icon-s-opportunity","el-icon-folder-opened","el-icon-paperclip","el-icon-mouse","el-icon-film"]
    return [{"icon": icon, "name":icon.replace("el-icon-","")} for icon in icons]