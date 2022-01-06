FROM python:3.10-slim-bullseye

RUN apt update && apt -y upgrade && apt -y dist-upgrade && \
    apt install -y python3-pip python3-dev python3-distutils build-essential

WORKDIR esc

COPY esc/*.py requirements.txt /esc/
COPY esc/config/config.json /esc/config/

COPY run_esc.bash /esc/
RUN chmod +x run_esc.bash

RUN pip3 install -r requirements.txt

WORKDIR cust_iface

COPY cust_iface/*.py /esc/cust_iface/
COPY cust_iface/project /esc/cust_iface/project
COPY cust_iface/auth /esc/cust_iface/auth
COPY cust_iface/ssl /esc/cust_iface/ssl

EXPOSE 8000

RUN ls -al

WORKDIR ../
RUN ls -al

# ENTRYPOINT [ "python3" ]
# CMD [ "main.py" ]
# CMD ["ls", "-al"]
CMD ["./run_esc.bash"]
