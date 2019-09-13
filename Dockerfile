# our base image
FROM ubuntu

RUN apt-get update
RUN apt-get -y -q install git
RUN apt-get -y -q install make
RUN apt-get -y -q install apt-utils

# specify the port number the container should expose
EXPOSE 8080

WORKDIR /home/work

