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

@Date: 2020-06-20 15:23:49
@Author: ashen23
@LastEditors: ashen_23
@LastEditTime: 2020-06-20 16:40:52
@FilePath: /mockAPI/tools/deleteProject.py
'''

import os
import sys

# 打印信息
def highlightPrint(text):
    print('\033[33m{}\033[0m'.format(text))

def deleteConfig(projectName):
    path = "../project/" + projectName + ".json"
    if not os.path.exists(path):
        highlightPrint("未查询到项目相关信息")
        return False
    os.remove(path)
    directories = "../jsons/" + projectName
    os.system("rm -rf " + directories)
    return True

def run(projectName):
    str = input("是否删除项目{}(此操作不可逆)? (yes, \033[4;32;40mno\033[0m):".format(projectName))
    if str == "yes":
        if deleteConfig(projectName):
            highlightPrint("🎉🎉🎉 移除项目<{}>成功".format(projectName))
    else:
        highlightPrint("用户取消操作")

if __name__ == '__main__':
    # 从api.ini 中加载数据
    if (len(sys.argv)) < 2:
        projectName = input("\033[31m请输入需要移除的项目名称:\033[0m")
        if len(projectName)>0:
            run(projectName)
    else:
        run(sys.argv[1])
