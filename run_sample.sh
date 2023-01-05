#!/bin/sh
docker-compose up -d
docker-compose exec -it python3 python sample.py
docker-compose stop