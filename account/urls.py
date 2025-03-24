from django.contrib import admin
from django.urls import path,include
from account.views import UserRegistration,Userlogin,UserProfile

urlpatterns = [
    
    path('register/', UserRegistration.as_view()),
    path('login/', Userlogin.as_view()),
    path('profile/', UserProfile.as_view()),
    
]
