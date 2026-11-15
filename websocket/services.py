
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class WebSocketService:

    @staticmethod
    def send_to_user(user_id, data):
        """Use from synchronous Django views."""
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "send.event",
                "data": data,
            }
        )

    @staticmethod
    async def send_to_user_async(user_id, data):
        """Use from async code."""
        channel_layer = get_channel_layer()

        await channel_layer.group_send(
            f"user_{user_id}",
            {
                "type": "send.event",
                "data": data,
            }
        )
