# PyApi

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

## run with docker

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
