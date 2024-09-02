from rest_framework_mongoengine import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .SuperUserModel.serializers import SuperUserSerializer
from .models import Freelancer, Client
from django.http import JsonResponse
from .serializers import *
import uuid
from django.views import View
#superuser api
class SuperUserSignUpView(generics.CreateAPIView):
    serializer_class = SuperUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#client and freelancer signup login apis
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

def generate_activation_token():
    """Generate a unique activation token"""
    return str(uuid.uuid4())

def email_exists(email):
    """Utility function to check if the email exists in either Freelancer or Client models."""
    return Freelancer.objects(email=email).exists() or Client.objects(email=email).exists()

class FreelancerSignUpView(generics.CreateAPIView):
    serializer_class = FreelancerSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        if email_exists(email):
            raise serializers.ValidationError({"email": "This email is already registered."})
        activation_token = generate_activation_token()
        serializer.save(activation_token=activation_token)

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
        activation_token = generate_activation_token()  # Generate the token
        serializer.save(activation_token=activation_token)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def find_user_by_activation_token(activation_token):
    try:
        # Check in the Client model
        user = Client.objects.get(activation_token=activation_token)
        return user
    except Client.DoesNotExist:
        pass
    
    try:
        # Check in the Freelancer model
        user = Freelancer.objects.get(activation_token=activation_token)
        return user
    except Freelancer.DoesNotExist:
        pass
    
    return None

@api_view(['GET'])
def check_activation_token_validity(request, activation_token):
    print(f"Received token: {activation_token}")
    
    # Find the user (client or freelancer) with the given activation token
    user = find_user_by_activation_token(activation_token)
    
    if user:
        if user.activation_token_valid:
            return Response({'valid': True, 'message': 'Activation token is valid.'}, status=200)
        else:
            return Response({'valid': False, 'message': 'Activation token has already been used.'}, status=400)
    else:
        return Response({'valid': False, 'message': 'Activation token is invalid.'}, status=404)

@api_view(['POST'])
def verify_activation(request, activation_token):
    
    # Find the user (client or freelancer) with the given activation token
    user = find_user_by_activation_token(activation_token)
    
    if user:
        if user.activation_token_valid:
            # Update user fields
            user.is_active = True
            user.activation_token_valid = False
            user.activation_token = ''
            user.save()
            
            return Response({'success': True, 'message': 'Your account has been activated successfully!'}, status=200)
        else:
            return Response({'success': False, 'message': 'Account is already activated.'}, status=400)
    else:
        return Response({'success': False, 'message': 'Activation token is not valid.'}, status=404)

def find_user_by_email(email):
    try:
        # Check in the Client model
        user = Client.objects.get(email=email)
        return user
    except Client.DoesNotExist:
        pass
    
    try:
        # Check in the Freelancer model
        user = Freelancer.objects.get(email=email)
        return user
    except Freelancer.DoesNotExist:
        pass
    
    return None

@api_view(['POST'])
def generate_password_reset_token(request):
    try:
        # Extract email from the request
        email = request.data.get('email')

        # Find the user by email
        user = find_user_by_email(email=email)
        
        # Generate a unique token
        token = uuid.uuid4().hex
        
        # Update user document with the token and set it as valid
        user.password_reset_token = token
        user.password_reset_token_valid = True
        user.save()
        
        # Optionally, you can send an email with the token to the user
        
        return JsonResponse({'message': 'Password reset token generated successfully', 'token': token}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User with this email does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def find_user_by_token(reset_token):
    try:
        # Check in the Client model
        user = Client.objects.get(password_reset_token=reset_token, password_reset_token_valid=True)
        return user
    except Client.DoesNotExist:
        pass
    
    try:
        # Check in the Freelancer model
        user = Freelancer.objects.get(password_reset_token=reset_token, password_reset_token_valid=True)
        return user
    except Freelancer.DoesNotExist:
        pass
    
    return None

class ValidateTokenView(View):
    def get(self, request, reset_token):
        try:
            # Find the user by password reset token in both Client and Freelancer models
            user = find_user_by_token(reset_token)
            if user:
                return JsonResponse({'valid': True}, status=200)
            else:
                return JsonResponse({'valid': False, 'error': 'Invalid or expired password reset token'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class ResetPasswordView(View):
    def post(self, request, reset_token):
        try:
            # Extract the new password from the request
            new_password = request.POST.get('password')
            if not new_password:
                return JsonResponse({'error': 'Password is required'}, status=400)

            # Find the user by password reset token
            user = find_user_by_token(reset_token)
            if not user:
                return JsonResponse({'error': 'Invalid or expired password reset token'}, status=404)

            # Hash the new password
            hashed_password = make_password(new_password)

            # Update the user document with the new password and invalidate the token
            user.password = hashed_password
            user.password_reset_token = ''
            user.password_reset_token_valid = False
            user.save()

            return JsonResponse({'message': 'Password has been reset successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)