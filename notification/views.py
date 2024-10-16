from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class TriggerNotif(APIView):
    def get(self, request):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "send_notif",
                "message": "You have a new notification"
            }
        )
        return Response({"message": "Notification sent."}, status.HTTP_200_OK)