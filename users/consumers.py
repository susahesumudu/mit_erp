import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user from the WebSocket scope
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            self.room_group_name = f'user_{self.user.id}'
            try:
                # Add the channel to the group
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.accept()  # Accept the WebSocket connection
                logger.info(f"WebSocket connection established successfully for user: {self.user.id}")
            except Exception as e:
                logger.error(f"Error during WebSocket connection for user {self.user.id}: {e}")
        else:
            # Close the connection if user is not authenticated
            await self.close()
            logger.warning("WebSocket connection closed due to unauthenticated user.")

    async def disconnect(self, close_code):
        # Remove the channel from the group on disconnect if authenticated
        if self.user.is_authenticated:
            try:
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
                logger.info(f"WebSocket connection closed for user {self.user.id} with code {close_code}.")
            except Exception as e:
                logger.error(f"Error during WebSocket disconnection for user {self.user.id}: {e}")

    async def receive(self, text_data):
        # Not used for notifications, but leaving it here in case it's needed in the future.
        try:
            data = json.loads(text_data)
            message = data.get('message', None)
            if message:
                logger.info(f"Received WebSocket data from user {self.user.id}: {message}")
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'send_notification',
                        'message': message,
                    }
                )
            else:
                logger.warning(f"Received invalid data from user {self.user.id}: Missing 'message' key.")
        except json.JSONDecodeError:
            logger.error(f"Failed to decode WebSocket message as JSON from user {self.user.id}.")
        except Exception as e:
            logger.error(f"Unexpected error in receive for user {self.user.id}: {e}")

    async def send_notification(self, event):
        # Send a message to the WebSocket
        message = event['message']
        try:
            await self.send(text_data=json.dumps({'message': message}))
            logger.info(f"Notification sent to user {self.user.id}: {message}")
        except Exception as e:
            logger.error(f"Error while sending notification to user {self.user.id}: {e}")

