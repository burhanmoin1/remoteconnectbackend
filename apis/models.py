from django_mongoengine import Document, EmbeddedDocument, fields
from datetime import datetime

class Message(EmbeddedDocument):
    sender = fields.StringField(blank=False)  # 'client' or 'freelancer'
    content = fields.StringField(blank=False)
    timestamp = fields.DateTimeField(default=datetime.now)

class Freelancer(Document):
    email = fields.EmailField(blank=False, unique=True)
    first_name = fields.StringField(blank=False)
    last_name = fields.StringField(blank=False)
    password = fields.StringField(blank=False)
    country = fields.StringField(blank=False)
    phone_number = fields.StringField(blank=True)
    agreed_to_terms = fields.BooleanField(default=False, blank=False)
    is_active = fields.BooleanField(default=False)
    activation_token = fields.StringField(blank=True)
    activation_token_valid = fields.BooleanField(blank=True, default=True)
    password_reset_token = fields.StringField(blank=True)
    password_reset_token_valid = fields.BooleanField(blank=True, default=False)
    session_tokens = fields.ListField(fields.StringField(), blank=True, default=list)

    meta = {
        'allow_inheritance': True,
        'indexes': ['email', 'password_reset_token', 'session_tokens', 'activation_token'],
    }

    def add_session_token(self, token):
        if len(self.session_tokens) < 4:
            self.session_tokens.append(token)
        else:
            self.session_tokens.pop(0)
            self.session_tokens.append(token)
        self.save()

    def remove_session_token(self, token):
        if token in self.session_tokens:
            self.session_tokens.remove(token)
            self.save()

    def is_session_token_valid(self, token):
        return token in self.session_tokens

class Client(Document):
    email = fields.EmailField(blank=False, unique=True)
    first_name = fields.StringField(blank=False)
    last_name = fields.StringField(blank=False)
    password = fields.StringField(blank=False)
    country = fields.StringField(blank=False)
    phone_number = fields.StringField(blank=True)
    agreed_to_terms = fields.BooleanField(default=False, blank=False)
    is_active = fields.BooleanField(default=False)
    activation_token = fields.StringField(blank=True)
    activation_token_valid = fields.BooleanField(blank=True, default=True)
    password_reset_token = fields.StringField(blank=True)
    password_reset_token_valid = fields.BooleanField(blank=True, default=False)
    session_tokens = fields.ListField(fields.StringField(), blank=True, default=list)

    meta = {
        'allow_inheritance': True,
        'indexes': ['email', 'password_reset_token', 'session_tokens', 'activation_token'],
    }

    def add_session_token(self, token):
        if len(self.session_tokens) < 4:
            self.session_tokens.append(token)
        else:
            self.session_tokens.pop(0)
            self.session_tokens.append(token)
        self.save()

    def remove_session_token(self, token):
        if token in self.session_tokens:
            self.session_tokens.remove(token)
            self.save()

    def is_session_token_valid(self, token):
        return token in self.session_tokens

class CFChat(Document):
    client = fields.ReferenceField(Client, blank=True)
    freelancer = fields.ReferenceField(Freelancer, blank=True)
    messages = fields.ListField(fields.EmbeddedDocumentField(Message), default=list)
    created_at = fields.DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            {'fields': ('client', 'freelancer'), 'unique': True}  # Ensures only one chat between a client and a freelancer
        ]
    }

class ChatRoom(Document):
    client = fields.ReferenceField('Client', blank=True)
    freelancer = fields.ReferenceField('Freelancer', blank=True)
    created_at = fields.DateTimeField(default=datetime.now)

    meta = {
        'indexes': ['client', 'freelancer'],
    }

class ChatMessage(Document):
    chat_room = fields.ReferenceField(ChatRoom, blank=True)
    sender = fields.StringField(blank=True)  # 'client' or 'freelancer'
    message = fields.StringField(blank=True)
    timestamp = fields.DateTimeField(default=datetime.now)

    meta = {
        'indexes': ['chat_room', 'timestamp'],
    }