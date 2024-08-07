from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime

# Create your models here.
class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    dueDate = models.DateTimeField(null=True, blank=True)
    reminderTime = models.DateTimeField(null=True, blank=True)
    
   
    
    
    def __str__(self):
        return self.title
    
class Reminder(models.Model):
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    sent = models.BooleanField(default=False)    