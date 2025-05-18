from concurrent import futures
import logging
import os
from dotenv import load_dotenv

import grpc
import message_pb2_grpc
from google.protobuf import empty_pb2
from azure.messaging.webpubsubservice import WebPubSubServiceClient

class MessageService(message_pb2_grpc.MessagingServicer):

    def __init__(self, pubsub : WebPubSubServiceClient):
        self.pubsub = pubsub

    def Send(self, request, unused_context):
        """It distributes the message to all users"""
        message = request.content
        logging.info(f"Message received: {message}")
        self.pubsub.send_to_all(message, content_type="text/plain")

        # This is the way the service returns nothing,
        # as message.proto describes
        return empty_pb2.Empty()

def serve():
    load_dotenv()
    connection_string = os.environ.get("CONNECTION_STRING")
    hub_name = os.environ.get("HUB")
    pubsub_client = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub_name)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MessagingServicer_to_server(MessageService(pubsub_client), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting message service")
    serve()