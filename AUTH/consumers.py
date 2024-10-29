import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.conf import settings

from AUTH.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name = 'chat'
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            for msg in await sync_to_async(lambda: list(Message.objects.order_by('-date_sent')[:settings.MIN_CHAT_MSGS_LOAD]))():
                await self.chat_message(msg)
        else:
            await self.send(text_data=json.dumps({
                'type': 'join error',
                'info': 'only registered users can send messages'
            }))
            await self.disconnect(0)

    async def disconnect(self, close_code: int):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)

        match data['type']:
            case 'send_message':
                if isinstance(data.get('content'), str):
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message_data': {
                                'type': 'message_sended',
                                'author_username': self.user.username,
                                'avatar_url': self.user.avatar.url,
                                'message_content': data['content'],
                            },
                        }
                    )
                    await sync_to_async(Message.objects.create)(author=self.user, content=data['content'], to=data['reply'])
                else:
                    await self.send(text_data=json.dumps({
                        'type': 'request error',
                        'info': 'request json must contains "content" string key',
                    }))

    async def chat_message(self, event):
        if isinstance(event, dict):
            data = event['message_data']
            await self.send(text_data=json.dumps({
                'type': 'message_sended',
                'author_username': data.get('author_username'),
                'avatar_url': data.get('avatar_url'),
                'message_content': data.get('message_content'),
            }))
        elif isinstance(event, Message):
            await self.send(text_data=json.dumps({
                'type': 'message_sended',
                'author_username': await sync_to_async(lambda: event.author.username)(),
                'avatar_url': await sync_to_async(lambda: event.author.avatar.url)(),
                'message_content': await sync_to_async(lambda: event.content)(),
            }))