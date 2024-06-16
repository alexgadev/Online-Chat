import os
import random

import yaml
from concurrent import futures

import grpc
import redis
#from ui import ui_handler
from proto import chat_pb2_grpc, chat_pb2


class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self, username):
        self.username = username # for several private chats opened at once

    def RegisterConnection(self, request, context):
        connect_chat(sender=username, receiver=f"{request.sender}:{request.address}")
        return chat_pb2.RegisterResponse(status="success")

    def SendMessage(self, request, context):
        #TODO: tratar la ip/puerto
        #TODO: printear en terminal del chat privado
        print(f"[{request.sender}] {request.message}")
        return chat_pb2.SendMessageResponse(status="success")
    

# option 1: connect chat
    # must provide an id of a private or group chat
    # check if id exists within the name server
        # open dedicated UI
        # check if it belongs to a single user
            # create connection to server stub through grpc
            # send and wait for messages
        # if it doesn't 
            # use RabbitMQ pubsub to send and wait for messages
    # if it doesn't, 
        # add id to the name server along with the conenction parameters as a group chat
        # create dedicated UI for the chat
        # send and wait for messages through RabbitMQ pubsub
    # -- IMPORTANT -- UI must provide means to leave a chat room
def connect_chat(self, sender, receiver):
    if not receiver:
        chat_id = input("Write the chat id: ")

        # access redis and retrieve connection parameters
        chat_params = redis_client.get(chat_id)

        if not chat_params:
            print("Chat doesn't exit or there was a typing error.")
        else:
            ip, port = chat_params.split(":")
    else:
        username, ip, port = receiver.split(":")

    # open gRPC channel to the receiver's server
    channel = grpc.insecure_channel(chat_params)

    # create the stub
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    if not receiver:
        # communicate username, ip and port to receiver through RegisterConnection
        request = chat_pb2.RegisterRequest(sender=sender.username, address=f"{self.ip}:{self.port}")
        stub.RegisterConnection(request)
    
    while True: # infinite loop for now, check if ESC has been pressed in order to leave chat 
        message = input(f"[{self.username}] ")
        request = chat_pb2.SendMessageRequest(sender=sender.username, message=message)
        response = stub.SendMessage(request)
        if not response.status == "success":
            return # gracefully end chat 
    # at some point loop ends and we can terminate the connection
    channel.close()
    

# option 2: subscribe to group chat
    # must provide an id
    # check existance of id within name server
        # open dedicated UI 
        # show messages sent to group chat's pubsub
        # UI must remove write privileges
    # if it doesn't exist
        # add new entry to the name server along with its connection parameters
        # open UI
        # listen for messages
def subscribe_chat():
    pass

# option 3: discover chats
def discover_chats():
    pass

# option 4: access insult channel
def access_insult_channel():
    pass


if __name__ == "__main__":
    # get username input from user keyboard
    username = input("Write your username: ")
    
    config_path = os.path.join('config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    redis_ip = config['name_server']['ip']
    redis_port = config['name_server']['port']
    redis_client = redis.Redis(host=redis_ip, port=redis_port, decode_responses=True)

    # check within name server if client ip has already been registered
        # if true retrieve another one
    #while existing_address(ip, port):
        # choose random client ip and port
    selected = random.choice(config['clients'])
    ip = selected['ip']
    port = selected['port']
    address = f'{ip}:{port}'

    keys = redis_client('*')
    for key in keys:
        if redis_client.get(key) == address:
            selected = random.choice(config['clients'])
            ip = selected['ip']
            port = selected['port']
            address = f'{ip}:{port}'
        else:
            break
    print(ip, port)

    # add entry to name server
    redis_client.set(username, address)

    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # use the generated function 'add_ChatServiceServicer_to_server'
    # to add the defined class to the server
    chat_pb2_grpc.add_ChatServiceServicer_to_server(
        ChatServicer(username=username), server)
    
    # lsiten on respective address and port
    server.add_insecure_port(address=address)

    server.start()

    opt = 0
    while opt != 0:
        #draw_menu()
        opt = input("hola")
        match opt:
            case 1: 
                # connect chat
                # ask for chat's id
                #connect_chat()
                pass
            case 2:
                # subscribe to group chat
                pass
            case 3:
                # discover chats
                pass
            case 4:
                # access insult channel
                pass

    server.wait_for_termination()