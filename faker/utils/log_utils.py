'''
@Date: 2020-06-24 11:26:50
@Author: ashen23
@LastEditors: ashen_23
@LastEditTime: 2020-07-14 11:15:01
@FilePath: /faker/utils/log_utils.py
'''
# 方便后续随时更换或者增加规则

import os
import logging
import logging.handlers
from utils.readconfig import ReadConfig

userConfig = ReadConfig()

logger = logging.getLogger("fakerlogger")
logger.setLevel(logging.DEBUG)

# 判断log文件是否存在
logFile = userConfig.logFile()
if not os.path.exists(logFile):
    newDir = os.path.dirname(logFile)
    if not os.path.exists(newDir):
        os.makedirs(newDir)
    open(logFile,'w')


rf_handler = logging.handlers.TimedRotatingFileHandler(filename=userConfig.logFile(),when='D',interval=1,backupCount=10)
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
logger.addHandler(rf_handler)


# 错误日志
def logError(error):
    logger.error(error)

# 信息日志
def logInfo(info):
    logger.info(info)

# debug 日志
def logDebug(debugInfo):
    logger.debug(debugInfo)
    print(debugInfo)
