FROM python:2

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y python-fontforge

CMD [ "python" ]
