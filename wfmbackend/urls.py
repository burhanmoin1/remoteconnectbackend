from django.urls import path
from apis.views import *

urlpatterns = [
    path('api/superusersignup/', SuperUserSignUpView.as_view(), name='superusersignup'),
    path('api/usersignup/', UserSignUpView.as_view(), name='usersignup'),

]
