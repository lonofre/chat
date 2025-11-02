import asyncio
import os
import websockets
import sys
from dotenv import load_dotenv
import grpc
import message_pb2
import message_pb2_grpc

from azure.messaging.webpubsubservice import WebPubSubServiceClient

async def connect(url):
    async with websockets.connect(url) as ws:
        print('connected')
        while True:
            print('Received message: ' + await ws.recv())

if __name__ == '__main__':
    # This is the example from Microsoft portal with
    # some tweaks. This script just receives message.
    # Therefore, it only tests whether the service
    # sends the messages correctly through PubSub or not.
    user = sys.argv[1]

    with grpc.insecure_channel('localhost:50052') as channel:
        stub = message_pb2_grpc.MessagingStub(channel)
        response = stub.GetConnectionUrl(message_pb2.Negotiation(id=user))

        try:
            asyncio.get_event_loop().run_until_complete(connect(response.url))
        except KeyboardInterrupt:
            pass