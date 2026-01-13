from django.urls import path
from .views import index, task_status, chat_view, chat_stream

urlpatterns = [
    path("", index, name="index"),
    path("task_status/", task_status, name="task_status"),
    path("chat/", chat_view, name="chat"),
    path("stream/", chat_stream, name="chat_stream"),
]
