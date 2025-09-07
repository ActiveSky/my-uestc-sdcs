#!/bin/bash

docker build -t mysimplekv:v1 .

docker-compose down
docker-compose up -d
