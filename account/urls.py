from django.contrib import admin
from django.urls import path,include
from account.views import UserRegistration,Userlogin

urlpatterns = [
    
    path('register/', UserRegistration.as_view()),
    path('login/', Userlogin.as_view()),
    
]
