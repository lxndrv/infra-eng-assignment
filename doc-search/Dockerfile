FROM python:3.10-slim-bullseye

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY samples /data

COPY src /app

WORKDIR /app
EXPOSE 8080
ENTRYPOINT [ "python3" ]
CMD [ "__init__.py", "/data" ]