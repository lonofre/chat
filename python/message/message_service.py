from concurrent import futures
import logging
from dotenv import load_dotenv

import grpc
import message_pb2_grpc
import message_pb2
from google.protobuf import empty_pb2

class MessageService(message_pb2_grpc.MessagingServicer):
    """A service that handles messages that users send."""

    def Send(self, request, unused_context):
        """It distributes the message to all users"""
        message = request.content
        user = request.user
        logging.info(f"Message received: {message} from {user}")

        # This is the way the service returns nothing,
        # as message.proto describes
        return empty_pb2.Empty()

    def GetConnectionUrl(self, request, unused_context):
        """Deprecated"""
        return message_pb2.UrlResponse(url="Unsupported")

def serve():
    load_dotenv()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MessagingServicer_to_server(MessageService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting message service")
    serve()
