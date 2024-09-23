from rest_framework_mongoengine import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .SuperUserModel.serializers import SuperUserSerializer
from .models import *
from django.http import JsonResponse
from .serializers import *
import uuid
from django.views import View
from .FreelancerBackend import FreelancerMongoEngineBackend
from .ClientBackend import ClientMongoEngineBackend
from django.contrib.auth.hashers import make_password, check_password
import json

@api_view(['POST'])
def check_password_api(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve the client based on email
        client = Client.objects.get(email=email)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the password is correct using check_password
    if check_password(password, client.password):
        return Response({'message': 'Password is correct'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

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
def check_email_api(request):
    data = json.loads(request.body)
    email = data.get('email')
    
    if not email:
        return JsonResponse({'error': 'Email is required.'}, status=400)
    
    user = find_user_by_email(email)
    
    if user:
        return JsonResponse({'exists': True}, status=200)
    else:
        return JsonResponse({'exists': False}, status=404)

@api_view(['POST'])
def generate_password_reset_token(request):
    try:
        # Extract email from the request
        email = request.data.get('email')

        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        # Find the user by email
        user = find_user_by_email(email=email)
        
        if user is None:
            return JsonResponse({'error': 'User with this email does not exist'}, status=404)
        
        # Generate a unique token
        token = uuid.uuid4().hex
        
        # Update user document with the token and set it as valid
        user.password_reset_token = token
        user.password_reset_token_valid = True
        user.save()
        
        # Optionally, you can send an email with the token to the user
        
        return JsonResponse({'message': 'Password reset token generated successfully', 'token': token}, status=200)
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

def reset_password(request, reset_token):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            new_password = data.get('password')

            if not new_password:
                return JsonResponse({'error': 'Password is required'}, status=400)

            # Find the user by password reset token
            user = find_user_by_token(reset_token)
            if not user:
                return JsonResponse({'error': 'Invalid or expired password reset token'}, status=404)

            # Debug: Print the new password for verification (only for debugging, remove in production)
            print(f"New password: {new_password}")

            # Hash the new password
            hashed_password = make_password(new_password)
            print(f"Hashed password: {hashed_password}")

            # Update the user document with the new hashed password and invalidate the reset token
            user.password = hashed_password
            user.password_reset_token = ''
            user.password_reset_token_valid = False
            user.save()

            # Debug: Verify password against stored hashed password (optional check)
            if check_password(new_password, user.password):
                print("Password verified successfully")
            else:
                print("Password verification failed")

            return JsonResponse({'message': 'Password has been reset successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@api_view(['POST'])
def check_login_email_api(request):
    data = request.data
    email = data.get('email')
    
    if not email:
        return JsonResponse({'error': 'Email is required.'}, status=400)
    
    # Check in Client collection
    client_exists = Client.objects.filter(email=email).exists()
    if client_exists:
        return JsonResponse({'exists': True, 'collection': 'Client'}, status=200)
    
    # Check in Freelancer collection
    freelancer_exists = Freelancer.objects.filter(email=email).exists()
    if freelancer_exists:
        return JsonResponse({'exists': True, 'collection': 'Freelancer'}, status=200)
    
    # Email not found in either collection
    return JsonResponse({'exists': False}, status=404)

@api_view(['POST'])
def client_login_api(request):
    # Extract data from the request
    data = request.data
    email = data.get('email')
    password = data.get('password')

    print(f"Received login request with email: {data}")

    # Authenticate using the Client backend
    user = ClientMongoEngineBackend().authenticate(request, email=email, password=password)

    if user is not None and user.is_active:
        session_token = str(uuid.uuid4())
        user.add_session_token(session_token)

        return Response({
            'message': 'Login successful',
            'name': user.first_name,
            'user_email': user.email,
            'user_id': str(user.pk),
            'session_token': session_token,
            'connected_user': 'Client'
        }, status=status.HTTP_200_OK)
    else:
         # Authentication failed or account not activated
        return Response({
            'error': 'Invalid email or password, or account not activated. Please check activation email.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def freelancer_login_api(request):
    # Extract data from the request
    data = request.data
    email = data.get('email')
    password = data.get('password')

    # Authenticate using the Freelancer backend
    user = FreelancerMongoEngineBackend().authenticate(request, email=email, password=password)

    if user is not None and user.is_active:
        session_token = str(uuid.uuid4())
        user.add_session_token(session_token)

        return Response({
            'message': 'Login successful',
            'name': user.first_name,
            'user_email': user.email,
            'user_id': str(user.pk),
            'session_token': session_token,
            'connected_user': 'Freelancer'
        }, status=status.HTTP_200_OK)
    else:
         # Authentication failed or account not activated
        return Response({
            'error': 'Invalid email or password, or account not activated. Please check activation email.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_session_checker(request):
    data = request.data
    email = data.get('email')
    session_token = data.get('session_token')

    if not email or not session_token:
        return Response({'error': 'Email and session token are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = None

    try:
        # Attempt to find the user in the Client model
        user = Client.objects.get(email=email)
        user_type = 'Client'
    except Client.DoesNotExist:
        try:
            # If not found, try the Freelancer model
            user = Freelancer.objects.get(email=email)
            user_type = 'Freelancer'
        except Freelancer.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the session token exists in the user's session tokens
    if user and session_token in user.session_tokens:
        return Response({'message': 'Session authenticated', 'user_type': user_type,}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Session not authenticated'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def initiate_chat(request):
    data = request.data
    client_email = data.get('client_email')
    freelancer_email = data.get('freelancer_email')

    try:
        client = Client.objects.get(email=client_email)
        freelancer = Freelancer.objects.get(email=freelancer_email)

        # Check if chat exists
        chat = CFChat.objects.filter(client=client, freelancer=freelancer).first()

        # Create new chat if it doesn't exist
        if not chat:
            chat = CFChat(client=client, freelancer=freelancer)
            chat.save()

        chat_id = str(chat.id)
        room_name = f'cfchat_{chat_id}'

        return Response({
            'chat_id': chat_id,
            'room_name': room_name
        }, status=status.HTTP_200_OK)

    except Client.DoesNotExist:
        return Response({'error': 'Client not found.'}, status=status.HTTP_400_BAD_REQUEST)
    except Freelancer.DoesNotExist:
        return Response({'error': 'Freelancer not found.'}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView

def freelancer_list_view(request):
    # Fetch all active freelancers
    freelancers = Freelancer.objects.filter(is_active=True)
    
    # Serialize data (adjust fields as necessary)
    freelancer_data = [
        {
            'id': str(freelancer.id),
            'first_name': freelancer.first_name,
            'last_name': freelancer.last_name,
            'email': freelancer.email,
            'country': freelancer.country
        }
        for freelancer in freelancers
    ]
    
    return JsonResponse(freelancer_data, safe=False)

@api_view(['POST'])
def create_or_get_chat_room(request):
    client_id = request.data.get('client_id')  # Use request.data for DRF requests
    freelancer_id = request.data.get('freelancer_id')

    try:
        # Retrieve the client and freelancer objects
        client = Client.objects.get(pk=client_id)
        freelancer = Freelancer.objects.get(pk=freelancer_id)

        # Check if a chat room already exists
        chat_room = ChatRoom.objects.filter(client=client, freelancer=freelancer).first()

        if chat_room is None:
            # Create a new chat room if it doesn't exist
            chat_room = ChatRoom(client=client, freelancer=freelancer)
            chat_room.save()

        # Return the chat room ID as a JSON response
        return JsonResponse({'chat_room_id': str(chat_room.id)}, status=200)

    except Client.DoesNotExist:
        return JsonResponse({'error': 'Client not found'}, status=404)
    except Freelancer.DoesNotExist:
        return JsonResponse({'error': 'Freelancer not found'}, status=404)

def get_chat_messages(request, chat_room_id):
    try:
        chat_room = ChatRoom.objects.get(pk=chat_room_id)
        messages = ChatMessage.objects.filter(chat_room=chat_room).order_by('timestamp')

        message_data = [
            {
                'sender': msg.sender,
                'message': msg.message,
                'timestamp': msg.timestamp.isoformat(),
            }
            for msg in messages
        ]
        return JsonResponse({'messages': message_data}, status=200)

    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Chat room not found'}, status=404)

@api_view(['POST'])
def send_message(request, chat_room_id):
    sender = request.data.get('sender')  # Use request.data for JSON payload
    message = request.data.get('message')

    if not sender or not message:
        return JsonResponse({'error': 'Sender and message are required'}, status=400)

    try:
        chat_room = ChatRoom.objects.get(pk=chat_room_id)

        chat_message = ChatMessage(
            chat_room=chat_room,
            sender=sender,
            message=message
        )
        chat_message.save()

        return JsonResponse({'success': 'Message sent'}, status=201)

    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Chat room not found'}, status=404)

@api_view(['GET'])
def check_chat_room_access(request, chat_room_id):
    user_id = request.GET.get('user_id')
    
    if not chat_room_id or not user_id:
        return JsonResponse({'error': 'Missing chat_room_id or user_id'}, status=400)

    try:
        chat_room = ChatRoom.objects.get(pk=chat_room_id)
        user_has_access = (chat_room.client.pk == user_id or chat_room.freelancer.pk == user_id)

        return JsonResponse({'has_access': user_has_access}, status=200)
    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Chat room does not exist'}, status=404)