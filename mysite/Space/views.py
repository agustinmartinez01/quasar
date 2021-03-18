from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
class SpaceViewSet(viewsets.ModelViewSet):
    def list(self, request):
        return {}