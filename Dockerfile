FROM ubuntu:trusty

RUN apt-get update && apt-get install -y fontforge

ENTRYPOINT ["/usr/bin/fontforge"]
