from django.urls import path
from apis.views import *

urlpatterns = [
    path('api/superusersignup/', SuperUserSignUpView.as_view(), name='superusersignup'),
    path('api/email_validator/', check_email, name='email_validator'),
    path('api/clientsignup/', ClientSignUpView.as_view(), name='clientsignup'),
    path('api/freelancersignup/', FreelancerSignUpView.as_view(), name='freelancersignup'),
]
