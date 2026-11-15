
import os
import asyncio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Edunexa.settings")

import django
django.setup()

from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator

from websocket.consumers import WebSocketConsumer
from websocket.services import WebSocketService


async def main():

    User = get_user_model()

    user, _ = await User.objects.aget_or_create(
        username="websocket_service_test"
    )

    communicator = WebsocketCommunicator(
        WebSocketConsumer.as_asgi(),
        "/ws/",
    )

    communicator.scope["user"] = user

    connected, _ = await communicator.connect()

    print("Connected:", connected)

    if not connected:
        return

    # Receive connection confirmation
    response = await communicator.receive_json_from()
    print("Connection response:", response)

    # Test ping/pong
    await communicator.send_json_to({
        "type": "ping",
    })

    response = await communicator.receive_json_from()
    print("Ping response:", response)

    # Test WebSocket service
    await WebSocketService.send_to_user_async(
    user.id,
    {
        "type": "test",
        "message": "Service working",
    }
)

    response = await communicator.receive_json_from(timeout=5)
    print("Service response:", response)

    await communicator.disconnect()


asyncio.run(main())
