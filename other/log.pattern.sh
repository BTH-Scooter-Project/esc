
###############################################################################################

##*****************##
##    pattern      ##
##*****************##

https://dbwebb.se/guide/docker

#################
# backend
#################

docker build -t neskoc/pattern:backend -f Dockerfile.api .
# or if Dockerfile exists
docker build -t neskoc/pattern:backend .
## publish on dockerhub
docker push neskoc/pattern:backend

docker run --rm  -p 1337:1337 -it neskoc/pattern:backend

## run on pattern_net
docker run --rm --net pattern_net -p 1337:1337 -it neskoc/pattern:backend

### ... with name
docker run --rm --net pattern_net --name backend -p 1337:1337 -it neskoc/pattern:backend

#################
# esc
#################

docker build -t neskoc/pattern:esc .

## publish on dockerhub
docker push neskoc/pattern:esc

## run on pattern_net
docker run --rm --net pattern_net -p 5000:5000 -it neskoc/pattern:esc


#################
# frontend
#################

docker build -t neskoc/pattern:frontend .

## publish on dockerhub
docker push neskoc/pattern:frontend
docker pull neskoc/pattern:frontend

## run on pattern_net
docker run --rm --net pattern_net -p 1338:1337 -it neskoc/pattern:frontend

#################
# running
#################

docker-compose up -d backend
docker-compose up frontend
docker-compose run esc

# clean up
docker-compose down

###############################################################################################

# Docker

docker images (alias: docker image ls)
docker login
docker ps
docker run --rm -it debian:bullseye-slim
docker stop elegant_dhawan
docker run f5567032a379
docker stop f5567032a379

# New Docker image

touch Dockerfile
nvim Dockerfile

# removing images / containers / cleaning up

## remove all stopped containers
docker rm  $(docker ps -q -a)

## remove all dangling images
docker rmi $(docker images -f "dangling=true" -q)

## remove container
docker rm f5567032a379

## remove image
docker rmi f5567032a379

docker system prune -a

#################
# docker network
#################

docker network ls
docker network create pattern_net
docker network inspect pattern_net

## remove network
docker network rm pattern_net

### ... with name
docker run --rm --net pattern_net --name esc -p 5000:5000 -it neskoc/esc:frontend
docker run --rm --net pattern_net --name frontend -p 1337:1337 -it neskoc/pattern:frontend

## publish on dockerhub
docker push

# clean up
docker-compose down
