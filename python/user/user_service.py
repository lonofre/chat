from concurrent import futures
import logging
import bcrypt

import grpc
import user_pb2_grpc
import user_pb2

"""Users that are using the app."""
passwords = {}

class UserService(user_pb2_grpc.UserServicer):
    def Create(self, request, unused_context):
        username = request.name
        if username in passwords:
            logging.info(f"User %s already exists")
            return user_pb2.CreateReply(success=False)

        if len(username) > 15:
            logging.info(f"User {username} has more than 15 characters. Not creating it")
            return user_pb2.CreateReply(success=False)

        logging.info(f"Creating new user {request.name}")

        # TODO: Hash the password
        password = request.password
        passwords[username] = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        return user_pb2.CreateReply(success=True)

    def Find(self, request, unused_context):
        logging.info(f"Finding user {request.name}")
        if request.name in passwords:
            logging.info(f"Found user {request.name}")
            return user_pb2.UserReply(user_exists=True)

        logging.info(f"User {request.name} not found")
        return user_pb2.UserReply(user_exists=False)

    def ValidateCredentials(self, request, unused_context):
        logging.info(f"Validating credentials for user {request.name}")
        username = request.name
        if not username in passwords:
            logging.info(f"User {username} does not exist")
            return user_pb2.ValidCredentialsReply(success=False, metadata={})

        password = request.password
        if not bcrypt.checkpw(password.encode("utf-8"), passwords[username]):
            logging.info(f"User {username} does not have the correct password")
            return user_pb2.ValidCredentialsReply(success=False, metadata={})

        return user_pb2.ValidCredentialsReply(success=True, metadata={})

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting user service')
    serve()
