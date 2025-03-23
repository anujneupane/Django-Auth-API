from rest_framework import serializers
from account.models import User

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User 
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only':True}
         }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Both Password Doesn't Match")
        return data   
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)       
    
class UserloginSerial(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email','password']

   