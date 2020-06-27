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

@Description: 主入口文件，接口解析
@Author: ashen23
@LastEditTime: 2020-06-24 16:41:43
@FilePath: /faker/faker/main.py
@Copyright: © 2020 Ashen23. All rights reserved.
'''

import json
import os
import socket
from pathlib import Path

from flask import Flask, jsonify, make_response, render_template, request,send_from_directory,redirect,url_for
from flask_restful import Api, Resource

from utils.file_utils import nameBy,allNameBy, pathBy, jsonPathBy, loadJson, writeJson, loadUrl
from utils.readconfig import ReadConfig
from utils.normal_utils import get_host_ip, groupIcons, resError, resSuccess, resNotFound
from utils.api_utils import ApiUtils
from utils.log_utils import  logDebug, logError, logInfo

app = Flask(__name__)
api = Api(app)

app.jinja_env.variable_start_string = '{{ '
app.jinja_env.variable_end_string = ' }}'
app.config['JSON_AS_ASCII'] = False

userConfig = ReadConfig()

class FetchRequest(Resource):
    def get(self):
        return featchJson(request)
        
    def post(self):        
        return featchJson(request)

# 根据url 获取json内容
def featchJson(request):
    logDebug("[fetch]url:{} {}".format(request.path, request.method))
    if Uapi.isDroped(request.path):
        return resNotFound()
    newUrl = jsonPathBy(request.path, request.method)
    # 根据不同参数获取对应json文件
    urlInfo = Uapi.getUrlModel(request.path)
    if all([urlInfo, urlInfo.param]) and len(urlInfo.param) > 0:
        print(urlInfo.param, urlInfo.paramType)
        if urlInfo.paramType == "Params":
            paramValue = request.args.get(urlInfo.param)
        elif urlInfo.paramType == "Body: form data":
            paramValue = request.form.get(urlInfo.param)
        elif urlInfo.paramType == "Body: x-www-form-urlencode":
            paramValue = request.form.get(urlInfo.param)
        elif urlInfo.paramType == "Body: raw":
            paramValue = request.json.get(urlInfo.param)
        else:
            return resError("参数类型错误: {} paramType:{}".format(request.path, urlInfo.paramType))
        
        if paramValue and len(paramValue)>0:
            name = nameBy(newUrl)
            method = "({})".format(request.method)
            newName = "{}{}-{}-{}".format(method, urlInfo.param, paramValue, name.replace(method, ""))
            name = newUrl.replace(name, newName)
            if Path(name).exists():
                newUrl = name
        else:
            return resError("必填参数不能为空:{}, type:{}".format(urlInfo.param,urlInfo.paramType))
    try :
        logDebug("[fetch]url:{} path:{}".format(request.path, newUrl))
        return loadJson(newUrl)
    except json.decoder.JSONDecodeError as err:
        return resError('json解析失败:\n{}'.format(err))


################## Page start ##################
# 首页
@app.route('/')
def home():
    return render_template('index.html',ip=get_host_ip(), icons=groupIcons(), sections=Uapi.urls(), title=userConfig.theme('title'))

# 接口详情界面
@app.route('/api_detail')
def api_detail():
    url = request.args.get('url')
    method = request.args.get('method')
    urlId = int(request.args.get("urlId", -1))
    url_info = Uapi.getUrlInfo(url, method, urlId)

    if not url_info:
        return render_template("404.html")
    return render_template('detail.html', result={"url": url, "urlInfo":url_info},title=url_info.get("desc"))

# 添加/修改 接口界面
@app.route('/add_request')
def add_request_page():
    url = request.args.get("url", "")
    method = request.args.get("method", "POST")
    urlId = int(request.args.get("urlId", -1))
    url_info = {"methods": Uapi.getMathods(),
                "sections": Uapi.getSectionsDesc(), 
                "urlInfo": Uapi.getUrlInfo(url, method, urlId),
                "state": "修改" if len(url)>0 else "添加"
                }

    if len(url)>0: # 修改url
        url_info["selectTitle"] = Uapi.getTitle(url)

    titleDesc = url_info.get("urlInfo").get("desc")
    title = "* " + (titleDesc if len(titleDesc)>0 else "添加接口")
    return render_template('add.html', url_info=url_info, title=title)
################## Page end ##################


################## API start ##################
# 添加或更新接口
@app.route('/addRequest', methods=['POST'])
def add_request():
    desc = request.json.get('desc')
    url = request.json.get('url')
    method = request.json.get('method')
    urlId = request.json.get("urlId", -1)

    paramName = request.json.get('paramName')
    paramValue = request.json.get('paramValues')
    paramJson = request.json.get('paramJson')
    paramType = request.json.get("paramType")

    if url.endswith('/'):
        return resError('url输入有误')

    # 处理带参数的接口
    if all([paramName,paramValue, paramJson]):
        # 验证json是否合理
        for i in range(len(paramValue)):
            if (len(paramJson)>i):
                error = json_not_validate(paramJson[i])
                if error:
                    return resError('({}:{}) 的json输入有误:{}'.format(paramName,paramValue[i],error))
            else:
                return resError('({}:{}) 的json输入有误'.format(paramName,paramValue[i]))
        Uapi.saveUrl(urlId, url, desc, method, paramName, paramType)
        # 将参数及json分别写入文件
        existURl = []
        for i in range(len(paramValue)):
            name = nameBy(url)
            newUrl = jsonPathBy(url, method).replace(name, paramName + '-' + paramValue[i] + '-' + name)
            existURl.append(newUrl)
            writeJson(newUrl, json.loads(paramJson[i]))
        # 移除
        Uapi.deleteOtherParam(url, method, paramName, existURl)
        return resSuccess()

    # 是否移除从多参数到无参数的 json 文件，目前不移除

    # 处理不带参数的接口
    return writeUrlJson(urlId, url, desc, method, request.json.get('content'))

@app.route('/deleteRequest', methods=["POST"])
def delete_request():
    Uapi.deleteUrl(request.json.get("urlId"), request.json.get("url"), request.json.get("method"))
    return resSuccess()


@app.route('/addGroup', methods=["POST"])
def addGroup():
    form = request.json.get("form")
    if not form.get("name"):
        return resError("name 不能为空")
    if not form.get("baseUrl"):
        return resError("baseUrl 不能为空")
    Uapi.addGroup(form)
    return resSuccess()

################## API end ##################

def json_not_validate(content):
    if not content:
        return "json content is nil"
    try:
        json.loads(content)
    except json.decoder.JSONDecodeError as error:
        return "{}".format(error)
    return None

# 写入json文件
def writeUrlJson(urlId, url, desc, method, content):
    if json_not_validate(content):
        return resError('json输入有误，请检查')
    # 写入缓存中
    error = Uapi.saveUrl(urlId, url, desc, method, "", "")
    if error:
        return resError(error)
    writeJson(jsonPathBy(url, method), json.loads(content))
    return resSuccess()

# 404 提醒
@app.errorhandler(404) 
def not_found(e):
    if Uapi.isCached(request.path):
        return featchJson(request)
    return resNotFound()

if __name__ == '__main__':
    # 从api.ini 中加载数据
    configPath = userConfig.api("apiFile")
    if not os.path.exists(configPath):
        print("\033[31m(config.ini)未找到配置文件:{}\n可先通过 tools/makeProject.py 创建项目再尝试\033[0m".format(configPath))
    else:
        Uapi = ApiUtils(configPath)

        # 判断参数是否合理
        if Uapi.validate():
            print("mock data error:" + Uapi.validate())

        print("\033[32mload config: {}\033[0m".format(configPath))

        api.add_resource(FetchRequest, *Uapi.loadAllUrls())
        app.debug = userConfig.isDebug()
        app.run(host='0.0.0.0', port=5000)
