from django.contrib.auth.backends import BaseBackend
from SuperUserModel.models import SuperUser
from django.contrib.auth.hashers import check_password

class MongoEngineBackend(BaseBackend):
    def authenticate(self, request, login=None, password=None):
        # Determine whether login is an email or username and fetch the user accordingly
        lookup = 'email' if '@' in login else 'username'
        try:
            superuser = SuperUser.objects.get(**{lookup: login})
        except SuperUser.DoesNotExist:
            return None

        # Check if the password matches
        if check_password(password, superuser.password):
            return superuser

        return None
