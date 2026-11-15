
import asyncio

from channels.testing import WebsocketCommunicator
from Edunexa.asgi import application


async def test_websocket():

    communicator = WebsocketCommunicator(
        application,
        "/ws/"
    )

    connected, subprotocol = await communicator.connect()

    print("Connected:", connected)

    if not connected:
        print("WebSocket connection failed")
        return

    response = await communicator.receive_json_from()
    print("Connection:", response)

    await communicator.send_json_to({
        "type": "ping"
    })

    response = await communicator.receive_json_from()
    print("Ping:", response)

    await communicator.send_json_to({
        "type": "test",
        "data": "Hello Edunexa"
    })

    response = await communicator.receive_json_from()
    print("Message:", response)

    await communicator.disconnect()


if __name__ == "__main__":
    asyncio.run(test_websocket())
