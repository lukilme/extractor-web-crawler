from django.urls import path
from .views import homepage_view

urlpatterns = [
    path("", hello_task),
]
