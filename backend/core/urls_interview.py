from django.urls import path
from .views import *

urlpatterns = [
    path('add/', addInterviews),
    path('get/', getInterviews),
    path('edit/<int:id>', editInterviews),
    path('search/', search),
]
