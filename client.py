# read yaml
# choose random client ip and port
# check within name server if client ip has already been registered
    # if true retrieve another one
import os
import yaml
import grpc
import random
import futures
#from ui import ui_handler
from proto import chat_pb2, chat_pb2_grpc


class ChatClient:
    def __init__(self, user, ip, port):
        self.username = user
        self.ip = ip
        self.port = port
    
    def connect_chat(self, receiver=False):
        if not receiver:
            chat_id = input("Write the chat id: ")
            # access redis and retrieve connection parameters
            # if chat_params:
                # continue
            # else:
                # show error message and get back to the menu
        else:
            # username, ip, port = receiver.split(":")
            pass
        # open gRPC channel to the receiver's server
        channel = grpc.insecure_channel(chat_params)

        # create the stub
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        if not receiver:
            # communicate username, ip and port to receiver through RegisterConnection
            request = chat_pb2.RegisterRequest(sender=self.username, address=f"{self.ip}:{self.port}")
            stub.RegisterConnection(request)
        
        while True: # infinite loop for now, check if ESC has been pressed in order to leave chat 
            message = input(f"[{self.username}] ")
            request = chat_pb2.SendMessageRequest(sender=self.username, message=message)
            response = stub.SendMessage(request)
            if not response.status == "success":
                return # gracefully end chat 
        # at some point loop ends and we can terminate the connection
        channel.close()

class ChatServicer(chat_pb2_grpc.ChatServiceServicer, ChatClient):
    def RegisterConnection(self, request, context):
        ChatClient.connect_chat(receiver=f"{request.sender}:{request.address}")
        return chat_pb2.RegisterResponse(status="success")
    
    def SendMessage(self, request, context):
        # tratar la ip/puerto
        # printear en terminal del chat privado
        print(f"[{request.sender}] {request.message}")
        return chat_pb2.SendMessageResponse(status="success")
    

if __name__ == '__main__':
    config_path = os.path.join('config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    selected = random.choice(config['clients'])
    ip = selected['ip']
    port = selected['port']
    print(ip, port)
    
    # get username input from user keyboard
    username = input("Write your username: ")

    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # use the generated function `add_InsultingServiceServicer_to_server`
    # to add the defined class to the server
    chat_pb2_grpc.add_ChatServiceServicer_to_server(
        ChatServicer(), server)

    # listen on respective address and port 
    server.add_insecure_port(f'{ip}:{port}')
    server.start()



# add entry to name server as follows redis.get(username) = ip, port

# infinite while loop
# draw_menu() as default state
# switch case depending on keyboard input
    # keyboard handler must be implemented for arrow keys and ESC


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

# option 3: discover chats
    