FROM debian:bullseye-slim


RUN apt update && apt -y upgrade && apt -y dist-upgrade && \
    apt install -y python3-pip python3-dev build-essential

WORKDIR esc

COPY esc/*.py esc/requirements.txt /esc/

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
