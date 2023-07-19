FROM ubuntu:latest
RUN apt update
RUN apt install kafkacat python3 pip -y
RUN pip install requests
ADD tombstone_connectors.py /

