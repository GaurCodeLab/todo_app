from rest_framework import serializers
from .models import ToDo
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')        
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}     
        
        
    def create(self, validated_data):
        user = User.objects.create_user(
           username= validated_data['username'],
            email =validated_data['email'],
            password=validated_data['password']
        )      
        return user  
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.CharField()
        self.fields.pop('username')
        
    def get_username_field(self):
        return 'email'
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')   
        
        print(f"Authenticating with email ={email} and password={password}")
        
        user = User.objects.get(email=email)
        if user and user.check_password(password):
            print('user found')
            refresh = self.get_token(user)
            data = {
                'refresh' : str(refresh),
                'access' : str(refresh.access_token),
            }
            return data
        else:
            print('user not found')
            print('user in database: ')
            for user in User.objects.all():
                print(user.email)
            raise AuthenticationFailed('Inavlid email or password')   
            
        # user = authenticate(email=email, password=password)
        
       
        
        
        
       
                        
         
        
       
        
       
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']    