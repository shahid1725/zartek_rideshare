# routing.py
from django.urls import path
from .consumers import RideTrackerConsumer

websocket_urlpatterns = [
    path('ride/<int:ride_id>/track/', RideTrackerConsumer.as_asgi()),
]
