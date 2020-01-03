FROM python:2

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y python-fontforge

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH /usr/local/lib/python2.7/site-packages

CMD [ "/usr/bin/python" ]
