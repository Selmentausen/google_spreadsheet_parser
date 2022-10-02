from django.http import JsonResponse
from rest_framework import viewsets

from .serializers import OrderSerializer
from .models import Order
from django.core.management import call_command


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


def update_data(request):
    call_command('updatedb')
    return JsonResponse({'success': 'OK'})
