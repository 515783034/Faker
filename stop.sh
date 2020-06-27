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
 # @Description: 停止本地服务器
 # @Author: ashen23
 # @LastEditTime: 2020-06-05 10:03:48
 # @FilePath: /MockApi/stop.sh
 # @Copyright: © 2020 Ashen23. All rights reserved.
###

#ps -ef|grep Python |grep -v grep| cut -c 9-15
ps x|grep Python |awk '{print $1}' | xargs kill -9

echo '关闭...'