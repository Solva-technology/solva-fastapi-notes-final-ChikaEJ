FROM python:3.13-slim

RUN apt-get update && apt-get upgrade -y

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]