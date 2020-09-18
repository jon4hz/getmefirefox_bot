FROM python:3.8-alpine
MAINTAINER jon4hz

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./getmefirefox_bot.py ./bot.py

CMD ["python", "./bot.py"]