from django.contrib import admin
from django.urls import path,include
from account.views import UserRegistration,Userlogin,UserProfile,UserPasswordChange,PasswordResetEmail

urlpatterns = [
    
    path('register/', UserRegistration.as_view()),
    path('login/', Userlogin.as_view()),
    path('profile/', UserProfile.as_view()),
    path('changepass/', UserPasswordChange.as_view()),
    path('emailReset/', PasswordResetEmail.as_view()),

]
