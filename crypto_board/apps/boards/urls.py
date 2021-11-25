from django.urls import path

from . import views

app_name = "boards"
urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("<id>", views.show, name="show"),
    path("<id>/edit", views.edit, name="edit"),
    path("<id>/share", views.share, name="share"),
    path("<id>/versions", views.versions, name="versions"),
    path("restore_version/<version_id>", views.restore_version, name="restore_version"),
]
