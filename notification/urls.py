from django.urls import path
from .views import TriggerNotif


urlpatterns = [
    path("", TriggerNotif.as_view()),
]
