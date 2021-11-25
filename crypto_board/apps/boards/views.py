import bleach
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from crypto_board.apps.boards.models import Board, BoardVersion
from .forms import BoardForm

@login_required
def index(request):
    boards = Board.objects.all().order_by('-created_at')
    return render(request, "boards/index.html", {'boards': boards})

@login_required
def show(request, id):
    board = Board.objects.get(pk=id)
    return render(request, "boards/show.html", {'board': board})

@login_required
def new(request):
    if request.method == 'GET':
        form = BoardForm()
        return render(request, "boards/new.html", {'form': form})
    elif request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            name = bleach.clean(form.cleaned_data["name"])
            board = Board(name=name, owner=request.user)
            board.set_reference_number()
            board.save()
            return redirect('boards:edit', id= board.id)

@login_required
def edit(request, id):
    board = Board.objects.get(pk=id)
    version = BoardVersion.objects.filter(board_id=board.id).latest('id')
    if version is None:
        print('Version none')
        version = BoardVersion(content="", board=board, modified_by=request.user)
    return render(request, "boards/edit.html", {'board': board, 'version': version})

@login_required
def board_versions(request, id):
    return render(request, "boards/board_versions.html")
