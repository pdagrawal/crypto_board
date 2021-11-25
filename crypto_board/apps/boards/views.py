from django.shortcuts import render

from crypto_board.apps.boards.models import Board

def index(request):
    boards = Board.objects.all().order_by('-created_at')
    return render(request, "boards/index.html", {'boards': boards})

def show(request, id):
    return render(request, "boards/show.html")

def edit(request, id):
    return render(request, "boards/edit.html")
