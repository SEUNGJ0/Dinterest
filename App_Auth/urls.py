from django.urls import path
from App_Auth.Auth_views import UserList
app_name = "App_Auth"

urlpatterns = [
    path('users', UserList.as_view(), name='users-list'),

]