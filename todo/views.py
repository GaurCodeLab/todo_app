from datetime import datetime
from django.conf import settings
from django.shortcuts import render
# from fastapi import Response
from rest_framework.response import Response
from rest_framework import generics
from .models import ToDo
from .serializers import MyTokenObtainPairSerializer, ToDoSerializer
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
import schedule
import time
from django.core.mail import send_mail
import threading
import environ
from celery import shared_task

class ToDoListCreate(generics.ListCreateAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            response_data = {'data': serializer.data}
            print("Response data:", response_data)
            return Response({'data':serializer.data})
        return Response(serializer.errors)
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response('Logout successfully')    
    
class ToDoDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer    
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = request.user.id
        todos = ToDo.objects.filter(user_id=user_id)
        serializer = ToDoSerializer(todos, many =True)
        response_data = serializer.data
        print("Response data:", response_data)
        return Response(serializer.data)
# Create your views here.


class ReminderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        todo = ToDo.objects.get(pk=pk)
        reminder_time = request.data.get('reminderTime')
        todo.reminderTime = datetime.datetime.strptime(reminder_time, '%Y-%m-%d %H:%M:%S')
        todo.save()
        
        
        #schedule the reminder
        send_reminder.apply_async((todo.id,), eta=todo.reminderTime)
        schedule.every().day.at(str(todo.reminderTime.time())).do(send_reminder, todo)
        
        #Run the scheduler in a separate thread
        threading.Thread(target=schedule.run_pending).start
        
        return Response({'message': 'Reminder scheduled successfully'}, status =200)
    
env = environ.Env()    

def send_reminder(todo):
    #send reminder notification to user
    subject = f'Reminder: {todo.title}'
    message = f'This is a reminder for your task: {todo.title}'
    from_email = env('EMAIL_HOST_USER')
    to_email = todo.user.email
    
    send_mail(subject, message, from_email, [to_email], fail_silently=False)
    print(f'Reminder: {todo.title}')    

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