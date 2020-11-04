import os, time
from flask import Blueprint, request,jsonify, send_from_directory, render_template
from utils.normal_utils import getLocalIp

bpResource = Blueprint('resource',__name__)
baseImgPath = "./static/images/uploaded/"

@bpResource.route("/index")
def index():
    uploadPath = getLocalIp() + "resource/uploadImage"
    return render_template('resource.html', resources=fetchResources(), uploadPath=uploadPath, title="资源")


@bpResource.route("/uploadImage", methods=["POST"])
def uploadImage():
    img = request.files.get('image')
    file_path = baseImgPath + img.filename
    img.save(file_path)

    imgUrl = getLocalIp() + "resource/images/" + img.filename
    return jsonify({"code":200, "data":{"image": imgUrl}})


@bpResource.route("/images/<name>")
def get_image(name):
    return send_from_directory(baseImgPath,name)


# 获取已上传的资源文件
def fetchResources():
    newFiles = []
    for root, _, files in os.walk(baseImgPath):
        for file in files:
            filepath = root + file
            fileinfo = os.stat(filepath)
            fileTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fileinfo.st_mtime))
            newFiles.append({'name': file, 'url': filepath, 'time':fileTime})
    return newFiles
