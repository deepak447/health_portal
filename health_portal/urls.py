from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # ...other URL patterns
    path('', include('accounts.urls')),
]