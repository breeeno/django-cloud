from django.contrib import admin
from django.urls import include, path

BASE_URL = 'api/v1/'


urlpatterns = [
    path(f"{BASE_URL}", include('src.users.urls')),
]
