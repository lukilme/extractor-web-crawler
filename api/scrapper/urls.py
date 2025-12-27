from django.urls import path
from .views import hello_task

urlpatterns = [
    path("hello/", hello_task),
]
