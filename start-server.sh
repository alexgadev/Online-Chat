#!/bin/bash

# Start Redis server
redis-server &

# Start RabbitMQ server
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management &

# Start the chat server
python server.py
