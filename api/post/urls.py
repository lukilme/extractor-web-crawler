from django.urls import path
from .views import feed, feed_api, feed_active

urlpatterns = [
    path("", feed, name="feed"),
    path("api/", feed_api, name="feed_api"),
    path("active/", feed_active, name="feed_active")
]
