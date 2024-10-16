from django.urls import path
from notification.consumers import NotificationConsumer


websocket_urlpatterns = [
    path("ws/notif/", NotificationConsumer.as_asgi()),
]