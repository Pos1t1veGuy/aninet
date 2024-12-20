import json
from datetime import datetime as dt
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.conf import settings

from AUTH.models import Message, User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = 'chat'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        for msg in await sync_to_async(lambda: list(Message.objects.order_by('-created_at')[:settings.MIN_CHAT_MSGS_LOAD:-1]))():
            await self.chat_message(msg)

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
                if self.user.is_authenticated:
                    if isinstance(data.get('content'), str):
                        created_at = dt.now()
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'chat_message',
                                'message_data': {
                                    'type': 'message_sended',
                                    'author_username': self.user.username,
                                    'timestamp': dt.timestamp(created_at),
                                    'avatar_url': self.user.avatar.url,
                                    'message_content': data['content'],
                                },
                            }
                        )
                        try:
                            reply = None if not data['reply'] else await sync_to_async(User.objects.get)(username=data['reply'])
                            await sync_to_async(Message.objects.create)(author=self.user, content=data['content'], to=reply, created_at=created_at)
                        except User.DoesNotExist:
                            await self.send(text_data=json.dumps({
                                'type': 'request error',
                                'info': 'reply username dows not exists',
                            }))
                    else:
                        await self.send(text_data=json.dumps({
                            'type': 'request error',
                            'info': 'request json must contains "content" string key',
                        }))
                else:
                    await self.send(text_data=json.dumps({
                        'type': 'join error',
                        'info': 'only registered users can send messages'
                    }))

    async def chat_message(self, event):
        if isinstance(event, dict):
            data = event['message_data']
            await self.send(text_data=json.dumps({
                'type': 'message_sended',
                'author_username': data.get('author_username'),
                'avatar_url': data.get('avatar_url'),
                'timestamp': data.get('timestamp'),
                'message_content': data.get('message_content'),
            }))
        elif isinstance(event, Message):
            await self.send(text_data=json.dumps({
                'type': 'message_sended',
                'author_username': await sync_to_async(lambda: event.author.username)(),
                'avatar_url': await sync_to_async(lambda: event.author.avatar.url)(),
                'message_content': await sync_to_async(lambda: event.content)(),
                'timestamp': dt.timestamp(await sync_to_async(lambda: event.created_at)()),
            }))