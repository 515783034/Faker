'''
@Description: 
@Author: ashen23
@LastEditTime: 2020-06-24 17:57:38
@FilePath: /faker/faker/utils/api_utils.py
@Copyright: © 2020 Ashen23. All rights reserved.
'''

import os
import json
import logging
from utils.file_utils import nameBy,allNameBy, pathBy,jsonPathBy, loadJson, loadFile, writeJson, loadUrl, deleteUrl, renameJson
from utils.jsonModel import jsonModel
from utils.models import ApiModel, ApiGroupModel, ApiUrlModel
from utils.log_utils import  logDebug, logError, logInfo

methods = ['POST','GET','HEAD','PUT']

# flask 没有内置数据库，需要用户安装，增加了复杂度
class ApiUtils:
    def __init__(self, path):
        self.apiPath = path
        if not os.path.exists(self.apiPath):
            return
        try:
            logging.info("从[{}]中加载参数成功".format(self.apiPath))
            json_info = json.loads(loadFile(path))
            self.model = ApiModel()
            self.model.fromJson(json_info)
            self.newId = json_info.get("newId")
        except:
            logDebug("加载参数出错")
        # 缓存接口
        self.cachedApi = []
        # 已移除的接口
        self.dropedApi = []

    '''
    @description: 验证加载参数是否正确
    '''
    def validate(self):
        if (self.model.project == "") | (self.model.newId == ""):
            return "{}:配置文件缺少project参数".format(self.apiPath)

    '''
    @description: 将所有接口更改存储到文件
    '''
    def saveUrls(self):
        writeJson(self.apiPath, self.model.toKeyValue())

    '''
    @description: 将新url信息保存到本地文件中
    @param {type} url信息
    '''
    def saveUrl(self, urlId, url, desc, method, param, paramType):
        logDebug("[api][save]url:{} {} {} {} {} {}".format(urlId, url, method, param, paramType, desc))
        baseUrl = pathBy(url)
        for group in self.model.groups:
            if baseUrl != group.baseUrl:
                continue
            # 当前分组新增数据
            if urlId == -1:
                return self._addNewUrl(urlId, url, desc, method, param, paramType, group)
            else:
                # 更新url
                return self._updateUrl(urlId, url, desc, method, param, paramType, group)
        
        # 默认在other新增
        if urlId == -1:
            return self._addNewUrl(urlId, url, desc, method, param, paramType, None)
        else: # 在 other 上更新
            return self._updateUrl(urlId, url, desc, method, param, paramType, group)

    '''
    @description: 删除某个url
    '''
    def deleteUrl(self, urlId, url, method):
        logDebug("[api][delete]url:{},{}".format(urlId, url))
        # 删除文件
        deleteUrl(url, method)
        # 删除ini中的数据
        self._deleteUrl(urlId)

        # 删除缓存中的数据
        for cache in self.cachedApi:
            if cache["id"] == urlId:
                self.cachedApi.remove(cache)
                return
        

    def deleteOtherParam(self, url, method, paramName, existUrls):
        name = nameBy(url)
        directory = jsonPathBy(url, method).replace(allNameBy(url, method),'')
        for file in os.listdir(directory):
            pathUrl = directory + file
            if file.startswith("({}){}-".format(method, paramName)) and file.endswith('-' + name) and (not pathUrl in existUrls):
                logDebug("[api][delete]param: {} {} {}".format(url, paramName, pathUrl))
                os.remove(pathUrl)


    def _addNewUrl(self, urlId, url, desc, method, param, paramType, group):
        logDebug("[api][add]url: {} {} {} {} {} {}".format(urlId, url, method, param, paramType, desc))
        if self._urlHasExist(url, group):
            return "请勿重复添加:" + url

        self.newId += 1
        newUrl = ApiUrlModel()
        newUrl.id = self.newId
        self.cachedApi.append({"id":self.newId, "url":url})
        newUrl.update(nameBy(url), url, desc, method, param, paramType)
        if group:
            group.urls.append(newUrl)
            self.saveUrls()
        else: # 默认添加的分组
            for aGroup in self.model.groups:
                if aGroup.desc == "other":
                    aGroup.urls.append(newUrl)
                    self.saveUrls()
                    return
            # 添加Other分组
            self._addOtherGroup(newUrl)
            
    def _updateUrl(self, urlId, url, desc, method, param, paramType, group):
        logDebug("[api][update]url: {} {} {} {} {} {}".format(urlId, url, method, param, paramType, desc))
        for urlInfo in group.urls:
            if urlInfo.id != urlId:
                continue
            if urlInfo.fullUrl != url: # 修改了methodName
                self.cachedApi.append({"id": urlId, "url":url})
                self.dropedApi.append(urlInfo.fullUrl)
                renameJson(urlInfo.fullUrl, url, method)
            # 方法名更改后，需要移除之前的文件
            if urlInfo.method != method:
                deleteUrl(urlInfo.fullUrl, urlInfo.method)
            # 修改值
            urlInfo.update(nameBy(url), url, desc, method, param, paramType)            
            # 兼容修改了url的情况
            duplicate = [cache for cache in self.cachedApi if cache.get("id") == urlInfo.id]
            if len(duplicate)>0:
                duplicate[0]["url"] = url
            self.saveUrls()
            return

    # 添加 other 分组
    def _addOtherGroup(self, url):
        logDebug("[api][add] group: [Other]")
        otherGroup = ApiGroupModel()
        otherGroup.name = "其他"
        otherGroup.icon = "el-icon-connection"
        otherGroup.desc = "other"
        otherGroup.urls = [url]
        self.model.groups.append(otherGroup)
        self.saveUrls()


    # 添加分组
    def addGroup(self, groupInfo):
        name = groupInfo.get("name")
        logDebug("[api][add] group: [{}]".format(name))
        group = ApiGroupModel()
        group.name = name
        group.desc = name
        group.icon = groupInfo.get("icon")
        group.baseUrl = groupInfo.get("baseUrl")
        self.model.groups.append(group)
        self.saveUrls()


    '''
    @description: 获取所有的 url(用于restful url)
    @return: [url]
    '''
    def loadAllUrls(self):
        urls = []
        for group in self.model.groups:
            urls.extend([url.fullUrl for url in group.urls])
        return urls

    def _urlHasExist(self, url, group):
        if not group:
            # 判断 other 中是否存在 url
            for group in self.model.groups:
                if group.desc == "other":
                    if len([x for x in group.urls if x.fullUrl == url]) <= 0:
                        return self.isCached(url)
                    return True
            return False

        if len([x for x in group.urls if x.fullUrl == url]) <= 0:
            return self.isCached(url)
        return True

    '''
    @description: 获取url对应的接口详细信息
    '''
    def getUrlInfo(self, url, method, urlId = -1):
        if (urlId == -1):
            return {"fullUrl": "", "desc": "", "method":""}
        
        for group in self.model.groups:
            if urlId != -1:
                urls = [x for x in group.urls if (x.id == urlId)]                
            else:
                urls = [x for x in group.urls if x.fullUrl == url]
            
            if len(urls) <= 0:
                continue
            urlInfo = urls[0].__dict__.copy()
            
            if len(urlInfo.get("param"))>0:
                param_values = self._getParamValues(url, urlInfo["param"], method)
                urlInfo["param_values"] = [value.get('param') for value in param_values]
                urlInfo["param_jsons"] = [value.get('content') for value in param_values]
                urlInfo["selectParamValue"] = urlInfo["param_values"][0]
            else:
                print("loadUrl", url, method)
                urlInfo["content"] = loadUrl(url, method)
            return urlInfo

    '''
    @description: 获取url信息
    '''
    def getUrlModel(self, url):
        for group in self.model.groups:
            if url.startswith(group.baseUrl):
                urls = [x for x in group.urls if x.fullUrl == url]
                if len(urls)>0:
                    print("######",urls[0])
                    return urls[0]
        return None

    '''
    @description: 获取所有分组接口
    @return: [section]
    '''
    def urls(self):
        return self.model.toKeyValue().get("groups")

    '''
    @description: 获取所有支持的方法名
    @return: [method]
    '''
    def getMathods(self):
        return methods

    '''
    @description: 获取分组的基本信息
    '''
    def getSectionsDesc(self):
        self.sections_desc = [{"name":group.name,"baseUrl":group.baseUrl} for group in self.model.groups]
        return self.sections_desc

    '''
    @description: 获取url所在分组的title
    '''
    def getTitle(self,url):
        path = pathBy(url)        
        titles = [section.get("name") for section in self.sections_desc if section.get("baseUrl") == path]
        return titles[0] if len(titles)>0 else ""

    '''
    @description: 当前url是否添加过
    '''
    def isCached(self, url):
        return len([cache for cache in self.cachedApi if cache.get("url") == url])>0

    '''
    @description: 接口是否已被移除
    '''
    def isDroped(self, url):        
        return url in self.dropedApi

    # 获取参数和json内容
    def _getParamValues(self, url, param, method):
        name = nameBy(url)
        directory = jsonPathBy(url, method).replace(allNameBy(url, method),'')

        result = []
        f_list = os.listdir(directory)
        prefix = "({}){}".format(method,param)
        for file in f_list:
            if file.startswith(prefix) & file.endswith(name):
                result.append({'param': file.split("-")[1], "content": loadFile(directory + file)})        
        return result

    def _deleteUrl(self, urlId):
        for group in self.model.groups:
            for urlInfo in group.urls:
                if urlInfo.id == urlId:
                    self.dropedApi.append(urlInfo.fullUrl)
                    group.urls.remove(urlInfo)
                    self.saveUrls()
                    return
