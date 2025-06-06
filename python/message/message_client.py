import message_pb2
import message_pb2_grpc

import grpc
import sys

def run(user: str, message: str):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = message_pb2_grpc.MessagingStub(channel)
        stub.Send(message_pb2.UserMessage(user=user, content=message))

if __name__ == '__main__':
    # This script sends a single message.
    try:
        user = sys.argv[1]
        message = sys.argv[2]
    except IndexError:
        user = "user"
        message = "Default message"

    run(user, message)