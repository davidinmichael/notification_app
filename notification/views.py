from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class TriggerNotif(APIView):
    def get(self, request):
        return Response({"message": "Notification sent."}, status.HTTP_200_OK)