from django.urls import path
from apis.views import *

urlpatterns = [
    path('api/superusersignup/', SuperUserSignUpView.as_view(), name='superusersignup'),
    path('api/email_validator/', check_email, name='email_validator'),
    path('api/clientsignup/', ClientSignUpView.as_view(), name='clientsignup'),
    path('api/freelancersignup/', FreelancerSignUpView.as_view(), name='freelancersignup'),
    path('api/verify-activation/<str:activation_token>/', verify_activation, name='verify_activation'),
    path('api/check-activation-token-validity/<str:activation_token>/', check_activation_token_validity, name='check_verification_token_validatity'),
    path('api/generate_password_reset_token/', generate_password_reset_token, name='generate_password_reset_token'),
    path('api/validate_token/<str:reset_token>/', ValidateTokenView.as_view(), name='validate_token'),
    path('api/reset_password/<str:reset_token>/', reset_password, name='reset_password'),
    path('api/client-login/', client_login_api, name='client-login'),
    path('api/freelancer-login/', freelancer_login_api, name='freelancer-login'),
    path('api/check-login-email/', check_login_email_api, name='check-email'),
    path('api/check-password/', check_password_api, name='check-password'),
    path('api/user_session_checker/', user_session_checker, name='user_session_checker'),
    path('api/getfreelancers/', freelancer_list_view, name='freelancer-list'),
    path('api/chatrooms/', create_or_get_chat_room, name='create-or-get-chat-room'),
    path('api/chatrooms/<str:chat_room_id>/messages/', get_chat_messages, name='get-chat-messages'),
    path('api/chatrooms/<str:chat_room_id>/messages/send/', send_message, name='send-message'),
    path('api/chatrooms/<str:chat_room_id>/check-access/', check_chat_room_access, name='check-chat-room-access'),
]
