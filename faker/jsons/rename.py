'''
@Date: 2020-07-15 09:08:59
@Author: ashen23
@LastEditors: ashen_23
@LastEditTime: 2020-07-15 10:20:37
@FilePath: /faker/jsons/rename.py
'''

import os


def loopFiles(filePath):
    # print(filePath)
    for file in os.listdir(filePath):
        realPath = filePath + "/" + file
        if os.path.isdir(realPath):
            loopFiles(realPath)
        else:
            newName = realPath
            if not realPath.endswith(".json"):
                newName += ".json"
            newName = newName.replace("(GET)","")
            newName = newName.replace("(POST)","")
            if "-" in file:
                last = file.split("-")[-1]
                ignoreFile = file.replace(last,"")
                newName = newName.replace(ignoreFile, "")
            print(realPath,newName)

            os.rename(realPath, newName)



if __name__ == "__main__":
    loopFiles("MockExample")