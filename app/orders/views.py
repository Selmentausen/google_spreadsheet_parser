from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets

from .serializers import OrderSerializer
from .models import Orders


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer