from django.urls import path
from .views import index, task_status, chat_view, chat_stream, homepage_view

urlpatterns = [
    path("", homepage_view, name="index"),
    path("task_id/", index, name="task_id"),
    path("task_status/", task_status, name="task_status"),
    path("chat/", chat_view, name="chat"),
    path("stream/", chat_stream, name="chat_stream"),
]
