FROM ubuntu:latest
RUN apt update -y  
RUN apt install docker.io haveged bash strace python3.8 python3-pip -y

COPY ./ ./
ARG ENV
RUN if [ "$ENV" = "dev" ] ; then pip3 install pybiolib-0.0.1.tar.gz; else pip3 install pybiolib; fi
RUN chmod +x run.sh
CMD ["/run.sh"]

