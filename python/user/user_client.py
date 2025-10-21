import logging
import sys

import grpc
import user_pb2
import user_pb2_grpc

def run(option: str, args):

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_pb2_grpc.UserStub(channel)

        if option == "-find":
            username = args[0]
            reply = stub.Find(user_pb2.UserExistsRequest(name=username))
            if not reply.user_exists:
                logging.info("User doesn't exist" )
            else:
                logging.info("User exists")
        elif option == "-create":
            username = args[0]
            password = args[1]
            reply = stub.Create(user_pb2.UserRequest(name=username, password=password))
            if not reply.success:
                logging.info("User couldn't be created")
            else:
                logging.info("User created")

        elif option == "-validate":
            username = args[0]
            password = args[1]
            reply = stub.ValidateCredentials(user_pb2.UserRequest(name=username, password=password))
            if not reply.success:
                logging.info("Invalid credentials")
            else:
                logging.info("Valid credentials")
                metadata = dict(reply.metadata)
                logging.info(metadata)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Client started")
    args = sys.argv[2:]
    option = sys.argv[1]
    run(option, args)
