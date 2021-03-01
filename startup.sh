#!/bin/bash

if [[ "$(docker images -q purple-cow_webapp:latest 2> /dev/null)" == "" ]]; then
  docker-compose build
fi

docker-compose up -d
