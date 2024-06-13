import os
import yaml
import grpc
import redis
import random
import asyncio
import futures
#from ui import ui_handler
from proto import chat_pb2, chat_pb2_grpc


class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self, username):
        self.username = username # for several private chats opened at once

    def RegisterConnection(self, request, context):
        connect_chat(receiver=f"{request.sender}:{request.address}")
        return chat_pb2.RegisterResponse(status="success")

    def SendMessage(self, request, context):
        #TODO: tratar la ip/puerto
        #TODO: printear en terminal del chat privado
        print(f"[{request.sender}] {request.message}")
        return chat_pb2.SendMessageResponse(status="success")
    
async def serve(address, username):
    # create a gRPC server
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    # use the generated function 'add_ChatServiceServicer_to_server'
    # to add the defined class to the server
    chat_pb2_grpc.add_ChatServiceServicer_to_server(
        ChatServicer(username=username), server)
    
    # lsiten on respective address and port
    server.add_insecure_port(address=address)
    await server.start()
    await server.wait_for_termination()


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
def connect_chat(self, sender, receiver=False):
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


if __name__ == '__main__':
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

    config_path = os.path.join('config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # check within name server if client ip has already been registered
        # if true retrieve another one
    while existing_address(ip, port):
        # choose random client ip and port
        selected = random.choice(config['clients'])
        ip = selected['ip']
        port = selected['port']
        print(ip, port)

    # get username input from user keyboard
    username = input("Write your username: ")

    # add entry to name server
    redis_client.set(username, f'{ip}:{port}')

    # run instance of server for entering requests of private chats
    asyncio.run(serve(f'{ip}:{port}'), username)

    opt = 0
    while opt != 0:
        draw_menu()
        opt = input()
        match opt:
            case 1: 
                # connect chat
                # ask for chat's id
                connect_chat()
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
    