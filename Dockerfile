FROM python:3.9-alpine
COPY requirements.txt /requirements.txt
RUN pip install  -r /requirements.txt && apk add nodejs

COPY ./ /app
WORKDIR /app

# update PATH environment variable

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
