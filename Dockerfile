FROM python:3.10-slim-bullseye

RUN apt update && apt -y upgrade && apt -y dist-upgrade && \
    apt install -y python3-pip python3-dev build-essential

WORKDIR esc

COPY esc/*.py requirements.txt /esc/
COPY esc/config/config.json /esc/config/

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
# CMD ["./local_ls.sh"]