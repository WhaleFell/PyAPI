FROM python:3.9-alpine
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt && apk add nodejs

COPY ./ /app
WORKDIR /app

# update PATH environment variable

CMD ["python3", "main.py"]
