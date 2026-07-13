from django.urls import path
from . import views

app_name = "scraper"

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("sources/", views.sources_list_view, name="sources_list"),
    path("sources/create/", views.source_create_view, name="source_create"),
    path("sources/<int:source_id>/edit/", views.source_edit_view, name="source_edit"),
    path(
        "sources/<int:source_id>/delete/",
        views.source_delete_view,
        name="source_delete",
    ),
    path("sources/<int:source_id>/run/", views.run_scraping_view, name="run_scraping"),
    path("jobs/", views.jobs_history_view, name="jobs_history"),
    path("news/", views.news_management_view, name="news_management"),
    path("news/<int:news_id>/edit/", views.news_edit_view, name="news_edit"),
    path("news/<int:news_id>/delete/", views.news_delete_view, name="news_delete"),
]
