from sys import prefix
from django.urls import path
from . import views

prefix = 'users'

urlpatterns = [
    path(f'{prefix}/register/',
         views.RegisterUserView.as_view(), name='register_user'),
    path(f'{prefix}/login/', views.login_user, name='login_user'),
    path(f'{prefix}/profile/',
         views.UserProfileView.as_view(), name='user_profile'),
    path(f'{prefix}/', views.UserList.as_view(), name='get_all_users')
]
