import asyncio
import os
import websockets
from dotenv import load_dotenv

from azure.messaging.webpubsubservice import WebPubSubServiceClient

async def connect(url):
    async with websockets.connect(url) as ws:
        print('connected')
        while True:
            print('Received message: ' + await ws.recv())

if __name__ == '__main__':
    # This is the example from Microsoft portal with
    # some tweaks

    load_dotenv()
    connection_string = os.environ.get("CONNECTION_STRING")
    hub_name = os.environ.get("HUB")

    service = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub_name)
    token = service.get_client_access_token()

    try:
        asyncio.get_event_loop().run_until_complete(connect(token['url']))
    except KeyboardInterrupt:
        pass