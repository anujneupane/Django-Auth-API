from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializer import UserSerializer

class UserRegistration(APIView):
    def post(self,request,formate = None):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg':'Registration Success'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            



