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
@LastEditTime: 2020-07-20 14:28:23
@FilePath: /faker/main.py
@Copyright: © 2020 Ashen23. All rights reserved.
'''

import json
import os
import socket
from pathlib import Path

from flask import Flask, render_template, request
from flask_restful import Api, Resource

from utils.api_utils import ApiUtils
from utils.readconfig import ReadConfig
from utils.file_utils import jsonPathBy, loadJson, writeJson, renameJson
from utils.normal_utils import getLocalIp, groupIcons, resError, resSuccess, resNotFound
from utils.log_utils import logDebug, logError, logInfo
from utils.models import initData, UrlModel
from modules.resource import bpResource

app = Flask(__name__)
api = Api(app)

app.jinja_env.variable_start_string = '{{ '
app.jinja_env.variable_end_string = ' }}'
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(bpResource,url_prefix='/resource')


initData()
userConfig = ReadConfig()

class FetchRequest(Resource):
    def get(self):
        return featchJson(request)
    def post(self):        
        return featchJson(request)

# 根据url 获取json内容
def featchJson(request):
    logDebug("[fetch]url:{} {}".format(request.path, request.method))
    
    urlModel = Uapi.getUrlByPath(request.path)
    if not urlModel:
        return resNotFound()
    if urlModel.method != request.method:
        return resError("请检查 GET 和 POST 请求是否正确")
    result = getJsonPath(request, urlModel)
    if result[0]:
        newUrl = result[1]
    else:
        return result[1]

    try:
        logDebug("[fetch]url:{} path:{}".format(request.path, newUrl))
        return loadJson(newUrl)
    except json.decoder.JSONDecodeError as err:
        return resError('json解析失败:\n{}'.format(err))

# 获取本地 json 文件地址
def getJsonPath(request,urlModel):
    newUrl = jsonPathBy(request.path)
    if len(urlModel.param) <= 0:
        return (True,newUrl)
    
    if urlModel.paramType == "Params":
        paramValue = request.args.get(urlModel.param)
    elif urlModel.paramType == "Body: form data" or urlModel.paramType == "Body: x-www-form-urlencode":
        paramValue = request.form.get(urlModel.param)
    elif urlModel.paramType == "Body: raw":
        paramValue = request.json.get(urlModel.param)
    else:
        return (False,resError("参数类型错误: {} paramType:{}".format(request.path, urlModel.paramType)))
    
    if paramValue and len(paramValue)>0:
        values = [model.value for model in urlModel.params if model.value == paramValue]
        newUrl = Uapi.pathWithParam(newUrl, paramValue)
        if len(values)<=0:
            allowValues = ",".join([model.value for model in urlModel.params])
            return (False, resError('{}参数错误,当前传入值:{},允许值:{}'.format(urlModel.param, paramValue, allowValues)))
        if Path(newUrl).exists():
            return (True,newUrl)
        else:
            return (False, resNotFound())
    else:
        return (False, resError("缺少必须参数:{}, type:{}".format(urlModel.param, urlModel.paramType)))


################## Page start ##################
# 首页
@app.route('/')
def home():
    ip = getLocalIp()
    sections = Uapi.groupsInfo()
    title = userConfig.theme('title')
    return render_template('index.html',ip=ip, icons=groupIcons(), sections=sections, title=title)

# 接口详情界面
@app.route('/api_detail')
def api_detail():
    urlId = int(request.args.get("urlId", -1))
    urlModel = Uapi.getUrlDetail(urlId)["urlInfo"]
    if not urlModel:
        return render_template("404.html")
    title = urlModel["name"]
    return render_template('detail.html', urlInfo=urlModel,title=title)

# 添加/修改 接口界面
@app.route('/add_request')
def add_request_page():
    urlId = int(request.args.get("urlId", -1))
    urlModel = Uapi.getUrlById(urlId)
    requestInfo = Uapi.getUrlDetail(urlId)
    title = "* " + (urlModel.name if urlModel else "添加接口")
    return render_template('add.html', url_info=requestInfo, title=title)
################## Page end ##################


################## API start ##################
# 添加或更新接口
@app.route('/addRequest', methods=['POST'])
def add_request():
    name = request.json.get('name')
    url = request.json.get('url').strip(" ")
    method = request.json.get('method')
    urlId = request.json.get("urlId", -1)
    groupUrl = request.json.get("groupName")

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
                error = jsonValidate(paramJson[i])
                if error:
                    return resError('({}:{}) 的json输入有误:{}'.format(paramName,paramValue[i],error))
            else:
                return resError('({}:{}) 的json输入有误'.format(paramName,paramValue[i]))
        param = {"name": paramName, "type":paramType, "values": paramValue}
        Uapi.saveUrl(urlId, url, name, method, param, groupUrl)
        # 将参数及json分别写入文件
        existURl = []
        for i in range(len(paramValue)):
            newUrl = Uapi.pathWithParam(url, paramValue[i])
            existURl.append(newUrl)
            writeJson(newUrl, json.loads(paramJson[i]))
        # 移除
        Uapi.deleteOtherParam(url, method, paramName, existURl)
        return resSuccess()

    # 是否移除从多参数到无参数的 json 文件，目前不移除
    # 处理不带参数的接口
    content = request.json.get('content')
    jsonError = jsonValidate(content)
    if jsonError:
        return resError('json输入有误，请检查')
    # 写入缓存中
    error = Uapi.saveUrl(urlId, url, name, method, {}, groupUrl)
    if error:
        return resError(error)
    writeJson(jsonPathBy(url), json.loads(content))
    return resSuccess()


@app.route('/deleteRequest', methods=["POST"])
def delete_request():
    Uapi.deleteUrl(request.json.get("urlId"))
    return resSuccess()


@app.route('/addGroup', methods=["POST"])
def addGroup():
    form = request.json.get("form")
    if not all([form.get("name"), form.get("baseUrl")]):
        return resError("name 或 baseUrl 不能为空")
    Uapi.addGroup(form)
    return resSuccess()

################## API end ##################

# 验证 json 文件是否符合规范
def jsonValidate(content):
    if not content:
        return "json content is nil"
    try:
        json.loads(content)
    except json.decoder.JSONDecodeError as error:
        print("json error: {}".format(error))
        print(content[19960:19990])
        return "{}".format(error)
    return None

# 404 提醒
@app.errorhandler(404) 
def not_found(e):    
    if Uapi.getUrlByPath(request.path):
        return featchJson(request)
    return resNotFound()

if __name__ == '__main__':
    # 从api.ini 中加载数据
    if not os.path.exists("config/faker.db"):
        print("\033[31m({})未找到\n可先通过 tools/makeProject.py 创建项目再尝试\033[0m".format(dbPath))
    else:
        project = userConfig.projectName()
        Uapi = ApiUtils(project)

        api.add_resource(FetchRequest, *Uapi.loadRestfulUrls())
        app.config["JSONIFY_MIMETYPE"] = "application/json;charsetutf-8"
        app.debug = userConfig.isDebug()
        app.run(host='0.0.0.0', port=5000)
