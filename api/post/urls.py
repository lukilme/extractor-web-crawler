from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.feed_view, name="feed"),
    path("news/<slug:slug>/", views.news_detail_view, name="detail"),
    path(
        "comment/<int:comment_id>/delete/",
        views.delete_comment_view,
        name="delete_comment",
    ),
]
