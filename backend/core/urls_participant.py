from django.urls import path
from .views import *

urlpatterns = [
    path('add/', addParticipants),
    path('get/', getParticipants),
]
