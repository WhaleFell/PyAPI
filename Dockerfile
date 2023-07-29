FROM python:3.9-alpine
COPY requirements.txt /requirements.txt
RUN pip install --user -r /requirements.txt

FROM base
# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./ /app
WORKDIR /app

# update PATH environment variable

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
