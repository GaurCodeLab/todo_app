from django.urls import path
from .views import LogoutView, ReminderView, ToDoListCreate, ToDoDetail, UserListView
from .views import RegisterView, MyTokenObtainPairView, MytokenRefreshView

urlpatterns = [
    path('todos/', ToDoListCreate.as_view(), name='todo-list-create'),
    path('todos/<int:pk>/', ToDoDetail.as_view(), name='todo-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MytokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('logout/', LogoutView.as_view(), name='logout-user'),
    path('todos/<int:pk>/reminder/', ReminderView.as_view(), name='todo-reminder'),
]

# print("todo/urls.py is being loaded")