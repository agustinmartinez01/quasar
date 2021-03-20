"""
    mysite URL Configuration
"""
from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers


router = routers.SimpleRouter()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('Space.urls')),
]
