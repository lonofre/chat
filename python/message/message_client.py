import message_pb2
import message_pb2_grpc
import logging

import grpc
import sys

def run(option: str, args):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = message_pb2_grpc.MessagingStub(channel)

        if option == "-send":
            # This option broadcast the message to a specific group
            user = args[0]
            message = args[1]
            group = args[2]
            stub.Send(message_pb2.UserMessage(user=user, content=message, group=group))

        elif option == "-negotiate":
            # This option ask for the connection url
            id = args[0]
            response = stub.GetConnectionUrl(message_pb2.Negotiation(id=id))
            print("url:", response.url)

        elif option == "-add-group":
            # This option adds an user to a group
            user = args[0]
            group = args[1]
            stub.AddUserToGroup(message_pb2.AddToGroupMessage(user=user, group=group))

if __name__ == '__main__':
    # This script sends a single message.
    # Or negotiates a url which the client
    # can use to connect with the WebSocket service.
    logging.basicConfig(level=logging.INFO)
    logging.info("Client started")
    args = sys.argv[2:]
    option = sys.argv[1]
    run(option, args)
