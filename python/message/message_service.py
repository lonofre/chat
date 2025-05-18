from concurrent import futures
import logging

import grpc
import message_pb2_grpc
from google.protobuf import empty_pb2

class MessageService(message_pb2_grpc.MessagingServicer):

    def Send(self, request, unused_context):
        """It distributes the message to all users"""
        message = request.content
        logging.info(f"Message received: {message}")
        # This is the way the service returns nothing,
        # as message.proto describes
        return empty_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MessagingServicer_to_server(MessageService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting message service")
    serve()