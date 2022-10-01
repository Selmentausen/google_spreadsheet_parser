from django.db import models

# Create your models here.
from django.db import models


class Orders(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    order_id = models.TextField()
    usd_cost = models.FloatField()
    rub_cost = models.FloatField()
    delivery_date = models.DateField(null=True)
