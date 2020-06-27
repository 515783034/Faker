#! /bin/sh

###
 #                        .::::.
 #                      .::::::::.
 #                     :::::::::::
 #                  ..:::::::::::'
 #               '::::::::::::'
 #                 .::::::::::
 #            '::::::::::::::..
 #                 ..::::::::::::.
 #               ``::::::::::::::::
 #                ::::``:::::::::'        .:::.
 #               ::::'   ':::::'       .::::::::.
 #             .::::'      ::::     .:::::::'::::.
 #            .:::'       :::::  .:::::::::' ':::::.
 #           .::'        :::::.:::::::::'      ':::::.
 #          .::'         ::::::::::::::'         ``::::.
 #      ...:::           ::::::::::::'              ``::.
 #     ````':.          ':::::::::'                  ::::..
 #                        '.:::::'                    ':'````..
 # 
 # @Description: 启动本地服务器
 # @Author: ashen23
 # @LastEditTime: 2020-06-24 10:41:15
 # @Copyright: © 2020 Ashen23. All rights reserved.
###


cd faker

if [ -d "./venv/" ];then
  source venv/bin/activate
else
  echo "正在安装环境所需依赖"
  python3 -m venv venv
  source venv/bin/activate
  pip3 install -r requirements.txt
fi

nohup python3 -u main.py> ../out.log 2>&1 &

echo "🎉🎉🎉启动成功..."
