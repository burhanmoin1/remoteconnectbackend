from django.urls import path
from apis.views import *

urlpatterns = [
    path('api/superusersignup/', SuperUserSignUpView.as_view(), name='superusersignup'),
    path('api/email_validator/', check_email, name='email_validator'),
    path('api/clientsignup/', ClientSignUpView.as_view(), name='clientsignup'),
    path('api/freelancersignup/', FreelancerSignUpView.as_view(), name='freelancersignup'),
    path('api/verify-activation/<str:activation_token>/', verify_activation, name='verify_activation'),
    path('api/check-activation-token-validity/<str:activation_token>/', check_activation_token_validity, name='check_verification_token_validatity'),
]
