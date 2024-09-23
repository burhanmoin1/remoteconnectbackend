from django.contrib.auth.backends import BaseBackend
from .models import Freelancer
from django.contrib.auth.hashers import check_password

class FreelancerMongoEngineBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            # Attempt to retrieve freelancer by email
            freelancer = Freelancer.objects.get(email=email)
        except Freelancer.DoesNotExist:
            return None

        # Check if the freelancer is active and if the password matches
        if freelancer and freelancer.is_active and check_password(password, freelancer.password):
            return freelancer  # Authentication successful
        return None  # Authentication failed

    def get_user(self, user_id):
        try:
            return Freelancer.objects.get(pk=user_id)
        except Freelancer.DoesNotExist:
            return None

