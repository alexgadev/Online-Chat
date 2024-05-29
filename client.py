
# register at launch: redis.get(username) = ip, port

# show options

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
    