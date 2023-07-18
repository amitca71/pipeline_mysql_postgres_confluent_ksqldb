FROM ubuntu:latest
RUN apt update
RUN apt install kafkacat python3 pip -y
RUN pip install requests
RUN alias python='python3'
COPY tumbersome_connectors.py /

