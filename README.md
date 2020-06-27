
Faker 用于一键搭建本地 mock data 服务，基于python3 + Flask。


## 特性
- [x] GET/POST 请求
- [x] 后台管理 [homepage](http://127.0.0.1:5000/)
- [x] 自定义参数类型(Params,form等)
- [x] 实时修改返回内容，即时生效
- [x] 一键搭建本地服务
- [ ] 快速批量导入接口


## 依赖

- [Python3](https://www.python.org/downloads)

## 安装与使用

### clone 项目

```Shell
git clone 
```

### 增加执行权限

```Shell
# 切换到当前路径
cd currentPath

# 增加执行权限
chmod 777 start.sh
chmod 777 stop.sh
```

### 运行

```Shell
# 运行
./start.sh

# 以调试模式运行
cd faker
source venv/bin/activate
python3 main.py

# 查看后台
http://127.0.0.1:5000/ 或 http://0.0.0.0:5000/
```

### 项目配置

项目配置文件的路径为 faker/config/config.ini，可自由配置

```
apiFile: 设置运行的project
```

## 相关工具

- tools/makeProject.py: 创建一个新的项目
    
    ```
    python3 tools/makeProject.py newProject
    ```
- toos/deleteProject.py: 移除当前已存在项目

    ```
    python3 tools/deleteProject.py someProject
    ```


## FAQ

### 手机如何访问 flask 本地服务器?

```Shell
# 手机和电脑在同一局域网下

# flask 的 host 需要设置为0:0:0:0, port(端口)随意

# 手机端通过"http://电脑ip:端口/***"访问API即可
```
