from django.urls import path

from . import views

app_name = "boards"
urlpatterns = [
    path("", views.index, name="index"),
    path("<id>", views.show, name="show"),
    path("<id>/edit", views.edit, name="edit"),
]
