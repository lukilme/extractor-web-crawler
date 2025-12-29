from django.urls import path
from .views import editor

urlpatterns = [
    path("editor/", editor),
]
