from concurrent import futures
import logging
import os
from dotenv import load_dotenv

import grpc
import message_pb2_grpc
import message_pb2
from google.protobuf import empty_pb2
from azure.messaging.webpubsubservice import WebPubSubServiceClient

class MessageService(message_pb2_grpc.MessagingServicer):
    """A service that handles messages that users send. Its job
    is to distribuite the message to all users that are subscribed to
    the chat hub."""

    def __init__(self, pubsub_service : WebPubSubServiceClient):
        self.pubsub_service = pubsub_service

    def Send(self, request, unused_context):
        content = request.content
        user = request.user
        group = request.group
        logging.info(f"Message received: {content} from {user}, group: {group}")

        message = {
            "from": user,
            "content": content,
            "group": group,
        }

        if group == "all":
            self.pubsub_service.send_to_all(message)
        else:
            self.pubsub_service.send_to_group(group, message)

        # This is the way the service returns nothing,
        # as message.proto describes
        return empty_pb2.Empty()

    def GetConnectionUrl(self, request, unused_context):
        id = request.id
        response = self.pubsub_service.get_client_access_token(user_id=id)
        url = response["url"]
        logging.info(f"Sending connection url for: {id}")
        return message_pb2.UrlResponse(url=url)

    def AddUserToGroup(self, request, unused_context):
        user = request.user
        group = request.group
        self.pubsub_service.add_user_to_group(group, user)
        logging.info(f"Added user {user} to group {group}")
        return empty_pb2.Empty()

def serve():
    load_dotenv()
    connection_string = os.environ.get("CONNECTION_STRING")
    hub_name = os.environ.get("HUB")
    pubsub_client = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub_name)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MessagingServicer_to_server(MessageService(pubsub_client), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting message service")
    serve()
