from concurrent import futures
import logging

import grpc
import user_pb2_grpc
import user_pb2

"""Users that are using the app."""
users = set()

class UserService(user_pb2_grpc.UserServicer):
    def Create(self, request, unused_context):
        username = request.name
        if username in users:
            logging.info(f"User %s already exists")
            return user_pb2.CreateReply(sucess=False)
        if len(username) > 15:
            logging.info(f"User {username} has more than 15 characters. Not creating it")
            return user_pb2.CreateReply(sucess=False)

        logging.info(f"Creating new user {request.name}")
        users.add(request.name)
        return user_pb2.CreateReply(sucess=True)

    def Find(self, request, unused_context):
        logging.info(f"Finding user {request.name}")
        if request.name in users:
            logging.info(f"Found user {request.name}")
            return user_pb2.UserReply(user_exists=True)
        logging.info(f"User {request.name} not found")
        return user_pb2.UserReply(user_exists=False)

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