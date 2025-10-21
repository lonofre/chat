from azure.communication.identity import CommunicationIdentityClient
from concurrent import futures
from dataclasses import dataclass
import logging
import bcrypt
from dotenv import load_dotenv
import os

import grpc
import user_pb2_grpc
import user_pb2
from google.protobuf import struct_pb2

@dataclass
class User:
    name: str
    password: bytes
    communication_id: str = ""

"""Users that are using the app."""
users = {}

class UserService(user_pb2_grpc.UserServicer):

    def __init__(self, client: CommunicationIdentityClient):
        self.client = client

    def Create(self, request, unused_context):
        username = request.name
        if username in users:
            logging.info(f"User %s already exists")
            return user_pb2.CreateReply(success=False)

        if len(username) > 15:
            logging.info(f"User {username} has more than 15 characters. Not creating it")
            return user_pb2.CreateReply(success=False)

        logging.info(f"Creating new user {request.name}")

        password = request.password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        new_user = User(name=username, password=hashed_password)
        users[username] = new_user

        return user_pb2.CreateReply(success=True)

    def Find(self, request, unused_context):
        logging.info(f"Finding user {request.name}")
        if request.name in users:
            logging.info(f"Found user {request.name}")
            return user_pb2.UserReply(user_exists=True)

        logging.info(f"User {request.name} not found")
        return user_pb2.UserReply(user_exists=False)

    def ValidateCredentials(self, request, unused_context):
        logging.info(f"Validating credentials for user {request.name}")
        username = request.name
        if not username in users:
            logging.info(f"User {username} does not exist")
            return user_pb2.ValidCredentialsReply(success=False, metadata={})

        password = request.password
        if not bcrypt.checkpw(password.encode("utf-8"), users[username].password):
            logging.info(f"User {username} does not have the correct password")
            return user_pb2.ValidCredentialsReply(success=False, metadata={})

        # Majority of this code comes from
        # https://learn.microsoft.com/en-us/azure/communication-services/quickstarts/identity/access-tokens
        identity_token_result = self.client.create_user_and_token(["voip"])
        identity = identity_token_result[0]
        token = identity_token_result[1].token
        id = identity.properties['id']
        metadata = {"token": token, "id": id}

        # As we define in the proto file, we should send a Struct,
        # we can't send a python dict
        struct_metadata = struct_pb2.Struct()
        struct_metadata.update(metadata)

        return user_pb2.ValidCredentialsReply(success=True, metadata=struct_metadata)

def serve():
    load_dotenv()
    connection_string = os.environ["COMMUNICATION_SERVICES_CONNECTION_STRING"]
    client = CommunicationIdentityClient.from_connection_string(connection_string)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServicer_to_server(UserService(client), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting user service')
    serve()
