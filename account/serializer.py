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

class UserProfileSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']

class UserChangePasswordSerial(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['password','password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Both Password Doesn't Match")
        user.set_password(password)
        user.save()
        return data       

class EmailPasswordResetserial(serializers.ModelField):
    email = serializers.EmailField(max_length = 255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['email']
