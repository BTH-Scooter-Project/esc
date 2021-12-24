#!/bin/bash

docker rm  $(docker ps -q -a)
docker-compose up backend

