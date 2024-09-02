from rest_framework_mongoengine import serializers
from django.contrib.auth.hashers import make_password
from .models import Freelancer, Client

class FreelancerSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Freelancer
        fields = '__all__'

    def create(self, validated_data):
        # Hash the password before saving the instance
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class ClientSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        # Hash the password before saving the instance
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)