#!/bin/sh
docker-compose up -d
docker-compose exec -it python3 python main.py
docker-compose stop