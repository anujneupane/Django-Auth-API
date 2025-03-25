from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializer import UserSerializer,UserloginSerial,UserProfileSerial,UserChangePasswordSerial,EmailPasswordResetserial
from rest_framework.authentication import authenticate
from account.renderer import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated 

# generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistration(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,formate = None):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Success'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            

class Userlogin(APIView):  
    renderer_classes = [UserRenderer]
    def post(self,request, format = None):
         serializer = UserloginSerial(data = request.data)
         if serializer.is_valid(raise_exception=True):
             email = serializer.data.get('email')
             password = serializer.data.get('password')
             user = authenticate(email = email,password=password)
             if user is not None:
              token = get_tokens_for_user(user)
              return Response({'token': token,'msg':'Login Success'},status=status.HTTP_200_OK)
             else:
              return Response({'msg':'Email or Password Not Valid '},status=status.HTTP_404_NOT_FOUND)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request, format = None):
        serializer = UserProfileSerial(request.user)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class UserPasswordChange(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request, format = None):
        serializer = UserChangePasswordSerial(data = request.data,context ={'user':request.user})
        if serializer.is_valid(raise_exception=True):
          return Response({'msg':'Password Change Success'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetEmail(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format = None):
        serializer = EmailPasswordResetserial(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset link Sent. Please Check your Email '},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

