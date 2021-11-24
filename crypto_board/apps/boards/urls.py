from django.urls import path

from . import views

app_name = "boards"
urlpatterns = [
    path("", views.index, name="boards"),
    path("<id>", views.show, name="board_details"),
    path("<id>/edit", views.edit, name="edit_board"),
]
