from rest_framework_mongoengine import generics
from rest_framework.response import Response
from rest_framework import status
from .SuperUserModel.serializers import SuperUserSerializer
from .models import Freelancer, Client
from django.http import JsonResponse
from .serializers import *

class SuperUserSignUpView(generics.CreateAPIView):
    serializer_class = SuperUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def check_email(request):
    email = request.GET.get('email', '').strip()
    
    if not email:
        return JsonResponse({'exists': False}, status=200)

    freelancer_exists = Freelancer.objects(email=email).exists()
    client_exists = Client.objects(email=email).exists()

    exists = freelancer_exists or client_exists

    if exists:
        return JsonResponse({'exists': True}, status=204)
    else:
        return JsonResponse({'exists': False}, status=200)


def email_exists(email):
    """Utility function to check if the email exists in either Freelancer or Client models."""
    return Freelancer.objects(email=email).exists() or Client.objects(email=email).exists()

class FreelancerSignUpView(generics.CreateAPIView):
    serializer_class = FreelancerSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        if email_exists(email):
            raise serializers.ValidationError({"email": "This email is already registered."})
        serializer.save()

    def post(self, request, *args, **kwargs):
        # Print or log the received form data
        print("Received form data:", request.data)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientSignUpView(generics.CreateAPIView):
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        if email_exists(email):
            raise serializers.ValidationError({"email": "This email is already registered."})
        serializer.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)