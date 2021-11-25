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
    board = Board.objects.get(reference=id)
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
            return redirect('boards:edit', id = board.id)

@login_required
def edit(request, id):
    board = Board.objects.get(reference=id)
    try:
        version = BoardVersion.objects.filter(board_id=board.id).latest('id')
    except BoardVersion.DoesNotExist:
        version = BoardVersion(content="", board=board, modified_by=request.user)
        version.save()
    return render(request, "boards/edit.html", {'board': board, 'version': version})

@login_required
def versions(request, id):
    board = Board.objects.get(reference=id)
    versions = board.versions().order_by('-created_at')
    return render(request, "boards/versions.html", {'board': board, 'versions': versions})

@login_required
def restore_version(request, version_id):
    version = BoardVersion.objects.get(pk=version_id)
    new_version = BoardVersion(content=version.content, board=version.board, modified_by=request.user)
    new_version.save()
    return redirect('boards:show', id = new_version.board.reference)
