FROM debian:buster-slim


RUN apt update && \
    apt install -y python3-pip python3-dev build-essential

WORKDIR esc

COPY esc /esc

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
