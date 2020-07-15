'''
@Description: 
@Author: ashen23
@LastEditTime: 2020-07-15 16:01:39
@FilePath: /faker/utils/api_utils.py
@Copyright: © 2020 Ashen23. All rights reserved.
'''

import os
import json
import logging
from utils.file_utils import nameBy,jsonPathBy, loadJson, loadUrl, deleteUrl, renameJson
from utils.jsonModel import jsonModel
from utils.log_utils import logDebug, logError, logInfo
from utils.models import fakerSession
from utils.models import UrlModel, GroupModel, ProjectModel, UrlParamModel

methods = ['POST','GET','HEAD','PUT']

class ApiUtils:
    def __init__(self, projectName):
        self.project = fakerSession.query(ProjectModel).filter(ProjectModel.name == projectName).first()
        if self.project:
            print(" \033[32mload config: {}\033[0m".format(projectName))
            print(" \033[32m首页地址可访问：http://127.0.0.1:5000\033[0m")
        else:
            logDebug("加载project:{}出错".format(projectName))

    def getUrlById(self, urlId):
        return fakerSession.query(UrlModel).filter(UrlModel.id == urlId).first()

    def getUrlByPath(self, path):
        return fakerSession.query(UrlModel).filter(UrlModel.url == path).first()

    # 根据名称获取 group(没有的话默认取 otherGroup)
    def getGroupByUrl(self, groupUrl):
        group = fakerSession.query(GroupModel).filter(GroupModel.baseUrl == groupUrl).first()
        return group if group else self.otherGroup()

    '''
    @description: 删除某个url
    '''
    def deleteUrl(self, urlId):
        urlModel = self.getUrlById(urlId)
        logDebug("[api][delete]url:{},{}".format(urlId, urlModel.url))
        # 删除文件
        deleteUrl(urlModel.url)
        fakerSession.delete(urlModel)
        fakerSession.commit()

    def deleteOtherParam(self, url, method, paramName, existUrls):
        name = nameBy(url)
        basePath = jsonPathBy(url)
        directory = os.path.dirname(basePath)
        for file in os.listdir(directory):
            pathUrl = directory + file
            if file.startswith(basePath) and (not pathUrl in existUrls):
                logDebug("[api][delete]param: {} {} {}".format(url, paramName, pathUrl))
                os.remove(pathUrl)

    # 添加分组
    def addGroup(self, groupInfo):
        name = groupInfo.get("name")
        logDebug("[api][add] group: [{}]".format(name))
        group = GroupModel(name=name,desc=name, icon=groupInfo.get("icon"), baseUrl=groupInfo.get("baseUrl"))
        self.project.groups.append(group)
        fakerSession.commit()
        return group

    def otherGroup(self):
        other = fakerSession.query(GroupModel).filter(GroupModel.desc == "other").first()
        return other if other else self.addGroup({"name": "其他","desc":"other", "icon":"el-icon-connection", "baseUrl":""})

    '''
    @description: 获取所有的 url(用于restful url)
    @return: [url]
    '''
    def loadRestfulUrls(self):
        urls = []
        for group in self.project.groups:
            urls.extend([url.url for url in group.urls])
        return urls

    # 获取带参数的接口的本地文件路径
    def pathWithParam(self, url, paramValue):
        return jsonPathBy(url).replace(".json", "-{}.json".format(paramValue))

    # 保存（新增/修改）接口信息到数据库
    def saveUrl(self, urlId, url, name, method, param, groupUrl):
        name = name if name else ""
        paramName = param.get("name", "")
        paramType = param.get("type", "")
        paramValues = param.get("values", [])

        if urlId == -1:
            if self.getUrlByPath(url):
                return "存在同名 url,请检查后重试"
            urlModel = UrlModel(url=url, name=name, method=method, param=paramName, paramType=paramType)
            self.urlAddParams(urlModel, paramValues)
        else:
            urlModel = self.getUrlById(urlId)
            # 若果修改了 url，需要修改对应的 json 文件
            if urlModel.url != url:
                renameJson(urlModel.url, url, urlModel.method)
            urlModel.url = url
            urlModel.name = name
            urlModel.method = method
            urlModel.param = paramName
            urlModel.paramType = paramType
            self.urlAddParams(urlModel, paramValues)
        
        group = self.getGroupByUrl(groupUrl)
        group.urls.append(urlModel)

        fakerSession.commit()

    # 更新 url 的参数
    def urlAddParams(self, urlModel, paramValues):
        # 移除旧的参数
        for oldParam in urlModel.params:
            fakerSession.delete(oldParam)
        # 添加新参数
        for value in paramValues:
            urlParam = UrlParamModel(value=value, url_id=urlModel.id)
            urlModel.params.append(urlParam)
    
    '''
    @description: 获取url对应的接口详细信息
    '''
    def getUrlDetail(self,urlId):
        if (urlId == -1):
            return self._emptyUrlDetail()
        
        urlModel = fakerSession.query(UrlModel).filter(UrlModel.id == urlId).first()
        if not urlModel:
            return self._emptyUrlDetail()

        result = urlModel.toDict()
        if urlModel.param != None and len(urlModel.params)>0:
            values = []
            jsons = []
            for param in urlModel.params:
                values.append(param.value)
                urlPath = self.pathWithParam(urlModel.url, param.value)
                jsons.append(loadUrl(urlPath))
            result["param_values"] = values
            result["param_jsons"] = jsons
            result["selectParamValue"] = values[0]
        else:
            result["content"] = loadUrl(urlModel.url)

        urlInfo = {
            "methods": self.getMethods(), 
            "sections": self.getSectionsDesc(), 
            "urlInfo": result,
            "state": "修改" if urlId != -1 else "添加"}
        
        if urlModel:
            urlInfo["selectTitle"] = urlModel.group.baseUrl

        return urlInfo

    # 新建接口时的信息
    def _emptyUrlDetail(self):
        return {
            "methods": self.getMethods(), 
            "sections": self.getSectionsDesc(), 
            "urlInfo": {"url": "", "name":"", "desc": "", "method":""},
            "state": "添加"}

    '''
    @description: 获取所有分组接口
    @return: [section]
    '''
    def groupsInfo(self):
        groups = []
        for group in self.project.groups:
            newGroup = group.toDict()
            newGroup["urls"] = [x.toDict() for x in group.urls]
            groups.append(newGroup)        
        return groups

    '''
    @description: 获取所有支持的方法名
    @return: [method]
    '''
    def getMethods(self):
        return methods

    '''
    @description: 获取分组的基本信息
    '''
    def getSectionsDesc(self):
        return [{"name":group.name,"baseUrl":group.baseUrl} for group in self.project.groups]