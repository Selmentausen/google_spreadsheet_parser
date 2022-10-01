from django.urls import path, include

from rest_framework import routers

from .views import OrderViewSet, update_data

app_name = 'orders'
router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('update_data/', update_data),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
