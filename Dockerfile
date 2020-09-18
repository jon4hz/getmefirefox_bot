FROM python:3.8-alpine
MAINTAINER jon4hz

WORKDIR /usr/src/app

RUN apk add gcc musl-dev libffi-dev openssl-dev python3-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./getmefirefox_bot.py ./getmefirefox_bot.py
COPY ./token.txt ./token.txt

CMD ["python", "./getmefirefox_bot.py"]
