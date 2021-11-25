from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from crypto_board.apps.boards.models import Board

@login_required
def index(request):
    boards = Board.objects.all().order_by('-created_at')
    return render(request, "boards/index.html", {'boards': boards})

@login_required
def show(request, id):
    board = Board.objects.get(pk=id)
    return render(request, "boards/show.html", {'board': board})

@login_required
def edit(request, id):
    return render(request, "boards/edit.html")

@login_required
def board_versions(request, id):
    return render(request, "boards/board_versions.html")
