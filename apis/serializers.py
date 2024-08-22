from rest_framework_mongoengine import serializers
from django.contrib.auth.hashers import make_password
from .models import Freelancer, Client, BaseUser

class BaseUserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'

    def create(self, validated_data):
        # Hash the password before saving the instance
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class FreelancerSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Freelancer

class ClientSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Client
