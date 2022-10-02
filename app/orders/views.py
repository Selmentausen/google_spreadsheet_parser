from django.shortcuts import render
from django.http import HttpResponse
from orders_api.models import Order
from django.core.management import call_command


# Create your views here.
def index(request):
    call_command('updatedb')
    orders = Order.objects.all()
    return render(request, "index.html", context={'orders': orders})
