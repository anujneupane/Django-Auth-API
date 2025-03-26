from rest_framework import serializers
from account.models import User
from xml.dom import ValidationErr
from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util

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

class EmailPasswordResetserial(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255,style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email']

    def validate(self,attrs):
        email = attrs.get('email') 
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('encoded uid',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('reset token',token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('reset link',link)


            # send email
            body ='Click Following Link to Reset Your Password'+link
            data = {
                'subject': 'Reset Your Password',
                'body' : body,  
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs 
        else:
            raise ValidationErr('You are not Registered User')
        
class FinalPasswordResetserial(serializers.Serializer):
    password = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, data):
        try:  
            password = data.get('password')
            password2 = data.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Both Password Doesn't Match")
            id = smart_str(urlsafe_base64_decode(uid))
            user =User.objects.get(id=id) 
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationErr("Token is not Valid or Expired")
            user.set_password(password)
            user.save()
            return data
        
        except DjangoUnicodeDecodeError as identifier:
              PasswordResetTokenGenerator().check_token(user,token)
              raise ValidationErr('Token is not Valid or Expired')
              

        
            
