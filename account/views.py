from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializer import UserSerializer

class UserRegistration(APIView):
    def post(self,request,formate = None):
        serializer = UserSerializer(data = request.data)
        return Response({'msg':'Registration Success'})


