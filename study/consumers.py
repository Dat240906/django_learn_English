import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OnlineUsersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("online_users", self.channel_name)
        await self.send(json.dumps({"type": "join"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("online_users", self.channel_name)
        await self.send(json.dumps({"type": "leave"}))

    async def receive(self, text_data):
        pass