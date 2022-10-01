from django.http import JsonResponse
from rest_framework import viewsets

from .serializers import OrderSerializer
from .models import Orders
from .api_calls.google_spreadsheet import get_spreadsheet_data
from .api_calls.usd_to_rub_exchange_rate import get_usd_to_rub_exchange_rate


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer


def update_data(request):
    spreadsheet_data = get_spreadsheet_data()
    exchange_rate = get_usd_to_rub_exchange_rate()
    for item_id, values in spreadsheet_data.items():
        order, _ = Orders.objects.update_or_create(id=item_id,
                                                   defaults={**values, 'rub_cost': values['usd_cost'] * exchange_rate})
        order.save()
    Orders.objects.exclude(id__in=spreadsheet_data.keys()).delete()
    return JsonResponse({'success': 'OK'})
