# PyApi

**WAN: The dev branch should not be used for production environments!**

BD7JDU BH7QZX

Base FastAPI Model to build.

## Feature

## Document

[FastAPI docs](https://fastapi.tiangolo.com/zh/)

## Reference

## Development

### >= Python3.8 Env

### Build Virtual Environment [ref](https://docs.python.org/3/library/venv.html)

windows:

```shell
python -m venv ./venv

# Open Powershell Limited
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate
.\venv\Scripts\Activate.ps1

# pip
pip install -r requirements.txt

# Eitx
deactivate 
```

### Install modul by pip

```shell
pip install "fastapi[all]"
pip install "uvicorn[standard]"
```

### Run Application

```shell
uvicorn main:app --reload
```

or..

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### run with docker

```shell
git clone https://github.com/WhaleFell/PyAPI.git

cd PyAPI

docker build -t my .

docker run -d --name PyAPI -p 8000:80 my

# 可更新代码
docker run -d --name PyAPI \
-v /root/PyAPI:/app/ \
-p 8000:80 \
my

docker restart PyAPI
```

### run with uvicorn or Gunicorn

[Uvicorn setting docs](https://www.uvicorn.org/settings/)

[FastAPI Docs server-workers](https://fastapi.tiangolo.com/deployment/server-workers/)

```shell
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4

# or..
# pip install gunicorn

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
```

## Develop with Git

```shell
# create dev branch
git branch dev
# checkout dev
git checkout dev
git checkout main
git checkout main
```

merge branch ignore some file

```shell
git config merge.ours.driver true

# .gitattributes
README.md merge=ours

git checkout main
git merge dev
```

## referent

ASGI (Asynchronous [eɪˈsɪŋkrənəs] Server Gateway Interface)  异步服务器网关接口  
WSGI (Web Server Gateway Interface) 网站服务器网关接口
