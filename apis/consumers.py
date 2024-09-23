import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Client, Freelancer, ChatRoom, ChatMessage
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']
        self.room_group_name = f'chat_{self.chat_room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender = text_data_json['sender']
        message = text_data_json['message']

        # Save message to the database
        await self.save_message(sender, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender,
                'message': message
            }
        )

    async def chat_message(self, event):
        sender = event['sender']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': sender,
            'message': message
        }))

    @sync_to_async
    def save_message(self, sender, message):
        # Find the chat room by ID
        try:
            chat_room = ChatRoom.objects.get(id=self.chat_room_id)
        except ChatRoom.DoesNotExist:
            raise ValidationError(f'Chat room with ID {self.chat_room_id} does not exist.')

        # Create and save the new chat message
        chat_message = ChatMessage.objects.create(
            chat_room=chat_room,
            sender=sender,
            message=message,
            timestamp=datetime.now()  # You can adjust this timestamp if needed
        )
        chat_message.save()
