from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_item, name='create_item'),
    path('read/<int:pk>/', views.read_item, name='read_item'),
    path('update/<int:pk>/', views.update_item, name='update_item'),
    path('delete/<int:pk>/', views.delete_item, name='delete_item'),
    
    # api for user
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    
    # path('register/',views.registerUser,name='register'),
    # path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

]