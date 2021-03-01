#!/bin/bash

if [[ ! -f .env ]]; then
  cp .docker/.env.template ./.env
fi

if [[ "$(docker images -q purple-cow_db:latest 2> /dev/null)" == "" ]]; then
  docker-compose build -f .docker/docker-compose.yml
else
  docker build -t purple-cow_db -f .docker/db/Dockerfile .
  docker build -t purple-cow_webapp -f .docker/webapp/Dockerfile .
fi

docker-compose -f .docker/docker-compose.yml up -d
