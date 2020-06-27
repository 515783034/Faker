'''
@Description: 
@Author: ashen23
@LastEditTime: 2020-06-24 15:58:03
@FilePath: /faker/faker/utils/models.py
@Copyright: © 2020 Ashen23. All rights reserved.
'''

from utils.jsonModel import jsonModel

@jsonModel()
class ApiUrlModel(object):
    def __init__(self):
        self.id = 0
        self.url = ""
        self.fullUrl = ""
        self.desc = ""
        self.method = ""
        self.param = ""
        self.paramType = ""

    def update(self, url, fullUrl, desc, method, param, paramType):
        self.url = url
        self.fullUrl = fullUrl
        self.desc = desc
        self.method = method
        self.param = param
        self.paramType = paramType


@jsonModel(listClassMap={"urls": ApiUrlModel})
class ApiGroupModel(object):
    def __init__(self):
        # 分组名
        self.name = ""
        # 分组图标, 查看https://element.eleme.cn/#/zh-CN/component/icon
        self.icon = ""
        # 分组文字描述
        self.desc = ""
        # 分组的前缀url
        self.baseUrl = ""
        # 所有url
        self.urls = []


@jsonModel(listClassMap={"groups":ApiGroupModel})
class ApiModel(object):
    def __init__(self):
        # 用户新增时确认id
        self.newId = ""
        # 项目名
        self.project = ""
        # api 分组
        self.groups = []