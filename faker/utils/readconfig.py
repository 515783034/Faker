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

@Description: 读取config.ini 配置内容
@Author: ashen23
@LastEditTime: 2020-07-15 16:15:55
@FilePath: /faker/utils/readconfig.py
@Copyright: © 2020 Ashen23. All rights reserved.
'''

import os
import configparser

ThemeSection = "Theme"
APISection = "API"
JSONSection = "JSON"
LOGSection = "LOG"

class ReadConfig:
    """定义一个读取配置文件的类"""

    def __init__(self, filepath=None):
        if filepath:
            configpath = filepath
        else:
            configpath = "config/config.ini"
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath)

    '''
    @description: 根据分组和参数返回对应值
    @return: 用户配置的数据
    '''
    def getParam(self, section, param):
        if self.cf.has_section(section) & self.cf.has_option(section, param):
            return self.cf.get(section, param)
        return ""

    ########################### 和业务相关逻辑的封装 ###########################

    def theme(self, param):
        return self.getParam(ThemeSection, param)
    
    def api(self, param):
        return self.getParam(APISection, param)

    def json(self, param):
        return self.getParam(JSONSection, param)

    def log(self, param):
        return self.getParam(LOGSection, param)

    def projectName(self):
        print("--{}--".format(self.api("project")))
        return self.api("project")

    def isDebug(self):
        if self.cf.has_section(APISection) & self.cf.has_option(APISection, "isDebug"):
            return self.cf.getboolean(APISection, "isDebug")
        return True

    def logFile(self):
        return self.log("logFile")