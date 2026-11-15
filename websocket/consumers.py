from channels.generic.websocket import AsyncJsonWebsocketConsumer


class WebSocketConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = self.scope["user"]

        # Authentication check
        if not self.user.is_authenticated:
            await self.close(code=4001)
            return

        # Accept connection
        await self.accept()

        # Send connection response
        await self.send_json({
            "type": "connection",
            "status": "connected",
            "message": "WebSocket connection established",
        })


    async def receive_json(self, content, **kwargs):

        # Validate JSON structure
        if not isinstance(content, dict):

            await self.send_json({
                "type": "error",
                "message": "Invalid message format",
            })

            return

        message_type = content.get("type")

        # Validate message type
        if not isinstance(message_type, str):

            await self.send_json({
                "type": "error",
                "message": "Message type is required",
            })

            return

        # Ping request
        if message_type == "ping":

            await self.send_json({
                "type": "pong",
            })

            return

        # Generic echo response
        await self.send_json({
            "type": "message",
            "data": content,
        })


    async def disconnect(self, close_code):

        # Connection cleanup
        pass