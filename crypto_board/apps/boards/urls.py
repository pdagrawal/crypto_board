from django.urls import path

from . import views

app_name = "boards"
urlpatterns = [
    path("", views.index, name="index"),
    path("<id>", views.show, name="show"),
    path("<id>/edit", views.edit, name="edit"),
    path("<id>/versions", views.board_versions, name="board_versions"),
]
