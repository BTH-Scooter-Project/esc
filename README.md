# esc

[![Python lint](https://github.com/BTH-Scooter-Project/esc/actions/workflows/Mockoon_Lint_and_test.yml/badge.svg)](https://github.com/BTH-Scooter-Project/esc/actions/workflows/Mockoon_Lint_and_test.yml)

[![Code Quality Grade](https://api.codiga.io/project/30675/score/svg)](https://api.codiga.io/project/30675/score/svg)
[![Code Grade](https://api.codiga.io/project/30675/status/svg)](https://api.codiga.io/project/30675/status/svg)

[![Unit test](https://github.com/BTH-Scooter-Project/esc/blob/main/coverage.svg)](https://github.com/BTH-Scooter-Project/esc/blob/main/coverage.svg)

## Docker

### Backend/API

```bash
# build and publish
docker build -t neskoc/pattern:backend -f Dockerfile.api .
docker push neskoc/pattern:backend

# run
docker run --rm  -p 1337:1337 -it neskoc/pattern:backend

## run on pattern_net
docker run --rm --net pattern_net -p 1337:1337 -it neskoc/pattern:backend

### ... with name
docker run --rm --net pattern_net --name backend -p 1337:1337 -it neskoc/pattern:backend
```

### esc

```bash

# build and publish
docker build -t neskoc/pattern:esc .
docker push neskoc/pattern:esc

## run on pattern_net
docker run --rm --net pattern_net -p 5000:5000 -it neskoc/pattern:esc
```

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


```yaml
version: "3"

networks:
    pattern_net:

# använd: docker build -t neskoc/pattern:backend -f Dockerfile.api . 
services:
    backend:
        image: neskoc/pattern:backend
        container_name: "backend"
        expose:
            - "1337"
        ports:
            - "127.0.0.1:1337:1337"
        networks:
            - pattern_net
        # volumes:
        #    - ./api:/api
        restart:
            "always"

    esc:
        image: neskoc/pattern:esc
        container_name: "esc"
        ports:
            - "127.0.0.1:8000:8000"
        networks:
            - pattern_net
        links:
            - backend
        depends_on:
            - backend

    admin:
        image: gusu20/admin-app
        container_name: "admin"
        ports:
            - "127.0.0.1:1338:1338"
        networks:
            - pattern_net
        links:
            - backend
        depends_on:
            - backend
        stdin_open: true

    app:
        image: Orkanen/myapp:latest
        container_name: "app"
        ports:
            - "127.0.0.1:1339:1339"
        networks:
            - pattern_net
        links:
            - backend
        depends_on:
            - backend

```
