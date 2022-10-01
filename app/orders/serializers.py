from rest_framework import serializers

from .models import Orders


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Orders
        fields = ('id', 'order_id', 'usd_cost', 'rub_cost', 'delivery_date')