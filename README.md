# django-vue-e_commerce

## 简述
哈尔滨工业大学（深圳）数据库系统实验三

本项目后端使用 Python 3.7，基于 Django 3.0.5 框架编写

前端使用 Vue.js，结合 BootstrapVue 编写。

>本项目采用前后端分离，为节省开发时间，后端允许跨域访问，关闭CSRF中间件，如不需要，请删除```./back_end/e_commerce/settings.py```中```INSTALLED_APPS```内的```'corsheaders'```，和```MIDDLEWARE```中的```'corsheaders.middleware.CorsMiddleware'```，并在```MIDDLEWARE```中添加```'django.middleware.csrf.CsrfViewMiddleware'```

>另外，后端的Debug模式已开启，关闭请将```./back_end/e_commerce/settings.py```中的```DEBUG=True```修改为```DEBUG=False```

## 运行方式

1. 后端

    ```sh
    $ cd ./back_end
    $ python3 -m venv env
    $ source ./env/bin/active
    (env)$ pip install -r requirements.txt
    (env)$ python3 manage.py runserver
    ```
    使用浏览器访问 [http://localhost:8000](http://localhost:8000)

2. 前端

    ```sh
    $ cd ./front_end
    $ npm install
    $ npm run serve
    ```
    使用浏览器访问 [http://localhost:8080](http://localhost:8080)
    
## 备注

本项目只是简单的Demo，部分核心功能未完成。
