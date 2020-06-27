'''
@Description: 根据模板文件生成一个项目
@Author: ashen23
@LastEditTime: 2020-06-20 17:59:16
@FilePath: /mockAPI/tools/makeProject.py
@Copyright: © 2020 Ashen23. All rights reserved.
'''

import os
import sys
import json

# 打印信息
def highlightPrint(text):
    print('\033[33m{}\033[0m'.format(text))


# 获取模板文件中配置的api
def getTemplateApis(template):
    groups = template.get("groups")
    apis = []
    if groups:
        for group in groups:
            for url in group.get("urls"):
                fullUrl = url.get("fullUrl")
                newUrl = fullUrl.replace(fullUrl.split("/")[-1], "({}){}".format(url.get("method"), fullUrl.split("/")[-1]))
                apis.append(newUrl)
    return apis

'''
@description: 生成接口文件
'''
def makeConfigJson(projectName):
    with open("../config/template.json", 'r', encoding="utf-8") as f:
        template = json.loads(f.read())
        template["project"] = projectName
        
        with open("../project/{}.json".format(projectName), 'w', encoding="utf-8") as w:
            w.write(json.dumps(template, indent=4, ensure_ascii=False))
            return template


'''
@description: 将字典保存到文件中
'''
def writeJson(name, json_content):
    new_dir = os.path.dirname(name)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    with open(name, 'w', encoding="utf-8") as file:
        file.write(json.dumps(json_content, indent=4, ensure_ascii=False))

'''
@description: 生成接口json文件
'''
def makeApiFiles(projectName, apis):
    for api in apis:
        jsonPath = '../jsons/{}{}'.format(projectName, api)
        writeJson(jsonPath, {"code":200, "errorMsg":"", "data":""})


def run(projectName):
    if os.path.exists("../project/{}.json".format(projectName)):
        highlightPrint("项目已存在，取消操作")
        return

    template = makeConfigJson(projectName)
    apis = getTemplateApis(template)
    makeApiFiles(projectName, apis)
    
    apiContent = "\n\t" + "\n\t".join(apis)
    runTip = "\n************\n修改 config/config.ini中的apiFile参数,重启以打开此项目"
    highlightPrint("🎉🎉🎉 新建项目<{}>成功, 创建接口如下{}".format(projectName, apiContent) + runTip)


if __name__ == '__main__':
    # 从api.ini 中加载数据
    if (len(sys.argv)) < 2:
        projectName = input("\033[33m请输入新建的项目名称:\033[0m")
        if len(projectName) > 0:
            run(projectName)
    else:
        run(sys.argv[1])

