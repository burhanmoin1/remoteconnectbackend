from django.contrib.auth.backends import BaseBackend
from .models import Client
from django.contrib.auth.hashers import check_password

class ClientMongoEngineBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            # Attempt to retrieve client by email
            client = Client.objects.get(email=email)
        except Client.DoesNotExist:
            return None

        # Check if the client is active and if the password matches
        if client and client.is_active and check_password(password, client.password):
            return client  # Authentication successful
        return None  # Authentication failed

    def get_user(self, user_id):
        try:
            return Client.objects.get(pk=user_id)
        except Client.DoesNotExist:
            return None
