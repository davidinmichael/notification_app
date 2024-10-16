from django.urls import path
from .views import NotificationConsumer


websocket_urlpatterns = [
    path("ws/notif/", NotificationConsumer.as_asgi()),
]