from django.db.models import fields
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     name= serializers.SerializerMethodField(read_only=True)
#     _id = serializers.SerializerMethodField(read_only=True)
#     isAdmin = serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model = User 
#         fields = ['id','_id','username','email','name','isAdmin']

#     def get__id(self,obj):
#         return obj.id

#     def get_isAdmin(self,obj):
#         return obj.is_staff

#     def get_name(self,obj):
#         name = obj.first_name
#         if name=="":
#             name = obj.email
#         return name


# class UserSerializerWithToken(UserSerializer):
#     token= serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model =User
#         fields = ['id','_id','username','email','name','isAdmin','token']

#     def get_token(self,obj):
#         token = RefreshToken.for_user(obj)
#         return str(token.access_token)

class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name', 'password', 'password2']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    validate_data.pop('password2', None)
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  password = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields = ['email', 'password']