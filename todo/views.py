from django.shortcuts import render
from rest_framework import generics
from .models import ToDo
from .serializers import MyTokenObtainPairSerializer, ToDoSerializer
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class ToDoListCreate(generics.ListCreateAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = [AllowAny]
    
class ToDoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer    
    permission_classes = [AllowAny]
# Create your views here.


class RegisterView(generics.CreateAPIView):
    # queryset =User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        print("request data: ", request.data)
        print("request headers:", request.headers)
        
        return super().post(request, *args, **kwargs)
    
    
class MytokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]    
    serializer_class = TokenRefreshView.serializer_class
    
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]    