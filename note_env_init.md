## 1、 创建虚拟环境
    python -m venv venv
## 2、进入虚拟环境
    # .\venv\Scripts\activate : 无法加载文件
    # 管理员身份进入WindowsPowerShell 
    # 输入Set-ExecutionPolicy PemoteSigned
    # 输入y
    # 重新进入虚拟环境即可
## 3、安装python包
    pip3 install -r requeirest.txt
## 4、命令行运行
    python -m flask run --host=0.0.0.0 --port=80
## 5、pycharm edit configuration 运行
    # module_name: flask
    # parameter: run --host=0.0.0.0 --port=80
    # environment variable: FLASK_APP=main;FALSK_ENV=development
