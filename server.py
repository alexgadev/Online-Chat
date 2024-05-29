import grpc
from concurrent import futures
import redis
import pika
import threading
from proto import chat_pb2_grpc, chat_pb2

# Configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672

# Redis client
