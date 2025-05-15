import logging
import sys

import grpc
import user_pb2
import user_pb2_grpc

def run(username: str):
    """Runs a test that mocks the client behavior:
    - It creates a user if the user doesn't exist
    - It prints a message if the user exists
    """
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_pb2_grpc.UserStub(channel)
        # Reply is the Message I defined in user.proto
        reply = stub.Find(user_pb2.UserRequest(name=username))
        if not reply.user_exists:
            stub.Create(user_pb2.UserRequest(name=username))
            logging.info('Created user %s', username)
        else:
            logging.info('User %s already exists', username)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Client started")
    try:
        username = sys.argv[1]
    except IndexError:
        username = "Gregg"
        logging.error(f"Name not provided. Defaulting to {username}")
    run(username)
