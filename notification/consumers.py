from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    group_notif = "notifications"
    chat_group = "chat_group"
    
    async def connect(self):
        await self.channel_layer.group_add(
            self.group_notif,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_notif,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get("type")

        if event_type == "chat_message":
            message = data.get("message")
            await self.channel_layer.group_send(
                self.chat_group,
                {
                    "type": "chat_message",
                    "message": message
                }
            )
        elif event_type == "send_notif":
            message = data.get("message")
            self.channel_layer.group_send(
                self.group_notif,
                {
                    "type": "send_notif",
                    "message": message
                }
            )
    
    async def send_notif(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": message
        }))
    
    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": message
        }))