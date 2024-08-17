from django_mongoengine import Document, fields
from datetime import datetime
import pytz

class SuperUser(Document):
    email = fields.EmailField(blank=False, unique=True)
    username = fields.StringField(blank=False, unique=True)
    first_name = fields.StringField(blank=False, unique=False)
    last_name = fields.StringField(blank=False, unique=False)
    password = fields.StringField(blank=False)
    is_active = fields.BooleanField(default=False)
    session_token = fields.StringField(blank=True, default='')

    def set_session_token(self, token):
        # Set the new session token, replacing any existing one
        self.session_token = token
        self.save()
    
    def remove_session_token(self):
        # Remove the current session token
        self.session_token = ''
        self.save()
    
    def is_session_token_valid(self, token):
        # Check if the provided token matches the current session token
        return self.session_token == token