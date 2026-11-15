
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class WebSocketConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close(code=4001)
            return

        self.group_name = f"user_{self.user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        await self.send_json({
            "type": "connection",
            "status": "connected",
        })

    async def disconnect(self, close_code):

        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive_json(self, content, **kwargs):

        if not isinstance(content, dict):
            await self.send_json({
                "type": "error",
                "message": "Invalid message format",
            })
            return

        if content.get("type") == "ping":
            await self.send_json({
                "type": "pong",
            })

    async def send_event(self, event):

        await self.send_json(event["data"])
