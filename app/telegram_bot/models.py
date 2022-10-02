from django.db import models


# Create your models here.
class TrackingOrders(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    user_id = models.IntegerField()
    order_id = models.TextField()
