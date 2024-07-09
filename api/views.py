from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from .models import Item
from .serializers import ItemSerializer
# from .serializers import UserSerializer, UserSerializerWithToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.shortcuts import get_object_or_404, render

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Data is saved"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    serializer = ItemSerializer(item)
    json_data = JSONRenderer().render(serializer.data)
    return Response(json_data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    serializer = ItemSerializer(item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, pk):
    item = Item.objects.get(pk=pk)
    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# JWT Views
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
       
#         serializer = UserSerializerWithToken(self.user).data

#         for k,v in serializer.items():
#             data[k] =v

#         return data
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         token['message'] = "Hello Proshop"
#         # ...

#         return token

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


# # SHOP API
# @api_view(['GET'])
# def getRoutes(request):
#     routes =[
#         '/api/products/',
#         '/api/products/<id>',
#         '/api/users',
#         '/api/users/register',
#         '/api/users/login',
#         '/api/users/profile',
#     ]
#     return Response(routes)

# from rest_framework.permissions import AllowAny
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def registerUser(request):
#     data = request.data
#     try:
#         user = User.objects.create(
#             first_name = data['name'],
#             username = data['email'],
#             password = make_password(data['password']),
#         )

#         serializer = UserSerializerWithToken(user,many=False)
#         return Response(serializer.data)
    
#     except:
#         message = {"detail":"User with this email is already registered"}
#         return Response(message,status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getUserProfile(request):
#     user =request.user 
#     serializer = UserSerializer(user,many = False)
#     return Response(serializer.data)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def updateUserProfile(request):
#     user =request.user 
#     serializer = UserSerializerWithToken(user,many = False)
#     data = request.data
#     user.first_name = data['name']
#     user.username = data['email']
#     user.email = data['email']
#     if data['password'] !="":
#         user.password= make_password(data['password'])
#     user.save()
#     return Response(serializer.data)

# @api_view(['DELETE'])
# def deleteUser(request,pk):
#     userForDeletion = User.objects.get(id=pk)
#     userForDeletion.delete()
#     return Response("User was deleted")

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


# class UserRegistrationView(APIView):
#   renderer_classes = [UserRenderer]
#   def post(self, request, format=None):
#     serializer = UserRegistrationSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.save()
#     token = get_tokens_for_user(user)
#     return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

# class UserLoginView(APIView):
#   renderer_classes = [UserRenderer]
#   def post(self, request, format=None):
#     serializer = UserLoginSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     email = serializer.data.get('email')
#     password = serializer.data.get('password')
#     user = authenticate(email=email, password=password)
#     if user is not None:
#       token = get_tokens_for_user(user)
#       return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
#     else:
#       return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['POST'])
# def create_item(request):
#     serializer = ItemSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         message = {"message":"data is saved"}
#         return render(request, 'operation.html', {'message': message})
#         # return Response(message, status=status.HTTP_201_CREATED)
#     message = {"data is not valid"}
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def create_item(request):
#     if request.method == 'POST':
#         serializer = ItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def read_item(request, pk):
#     item = get_object_or_404(Item, pk=pk)
#     serializer = ItemSerializer(item)
#     return Response(serializer.data)


# @api_view(['PUT'])
# def update_item(request, pk):
#     item = get_object_or_404(Item, pk=pk)
#     if request.method == 'PUT':
#         serializer = ItemSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['DELETE'])
# def delete_item(request, name):
#     item = get_object_or_404(Item, name=name)
#     item.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['DELETE'])
# def deleteUser(request,pk):
#     userForDeletion = User.objects.get(id=pk)
#     userForDeletion.delete()
#     return Response("User was deleted")