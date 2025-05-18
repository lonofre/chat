import message_pb2
import message_pb2_grpc

import grpc
import sys

def run(message: str):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = message_pb2_grpc.MessagingStub(channel)
        stub.Send(message_pb2.UserMessage(content=message))

if __name__ == '__main__':
    try:
        message = sys.argv[1]
    except IndexError:
        message = "Default message"

    run(message)