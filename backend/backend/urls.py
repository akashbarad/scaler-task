from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('interview/', include('core.urls_interview')),
    path('participant/', include('core.urls_participant')),
]
