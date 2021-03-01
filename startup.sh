#!/bin/bash

if [[ "$(docker images -q purple-cow_db:latest 2> /dev/null)" == "" ]]; then
  docker-compose build
else
  docker build -t purple-cow_db -f .docker/db/Dockerfile .
  docker build -t purple-cow_webapp -f .docker/webapp/Dockerfile .
fi

docker-compose up -d
