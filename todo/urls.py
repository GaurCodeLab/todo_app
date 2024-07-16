from django.urls import path
from .views import ToDoListCreate, ToDoDetail

urlpatterns = [
    path('todos/', ToDoListCreate.as_view(), name='todo-list-create'),
    path('todos/<int:pk>/', ToDoDetail.as_view(), name='todo-detail'),
]
