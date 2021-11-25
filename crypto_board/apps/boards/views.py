from django.shortcuts import render

from crypto_board.apps.boards.models import Board

def index(request):
    boards = Board.objects.all().order_by('-created_at')
    return render(request, "boards/index.html", {'boards': boards})

def show(request, id):
    board = Board.objects.get(pk=id)
    return render(request, "boards/show.html", {'board': board})

def edit(request, id):
    return render(request, "boards/edit.html")

def board_versions(request, id):
    return render(request, "boards/board_versions.html")
