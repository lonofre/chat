# Messaging

For testing, you should follow this order:

1. Run `message_service.py`, which handles the gRPC service. Also, this service push messages through the PubSub client.
2. Run `receiver.py`, which just receives messages.
3. Run `message_client.py [FROM] [MESSAGE]` to send messages.

   - `[FROM]` is the person/entity who is sending the message.
   - `[MESSAGE]` is the message's content.