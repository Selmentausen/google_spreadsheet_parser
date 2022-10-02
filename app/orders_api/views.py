from django.http import JsonResponse
from rest_framework import viewsets

from .serializers import OrderSerializer
from .models import Order
from django.core.management import call_command
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['id', 'order_id']


def update_data(request):
    call_command('updatedb')
    return JsonResponse({'success': 'OK'})
