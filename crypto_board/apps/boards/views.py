import bleach
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mirage.crypto import Crypto

from django.contrib.auth.models import User
from crypto_board.apps.boards.models import Board, BoardVersion, BoardUser
from .forms import BoardForm

@login_required
def index(request):
    boards_ids = list(Board.objects.filter(owner_id = request.user.id).values_list('id', flat=True))
    boards_ids += list(BoardUser.objects.filter(user = request.user.id).values_list('board_id', flat=True))
    boards = Board.objects.filter(pk__in=boards_ids).order_by('-created_at')
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
            c = Crypto()
            name = c.encrypt(bleach.clean(form.cleaned_data["name"]))
            board = Board(name=name, owner=request.user)
            board.set_reference_number()
            board.save()
            board_user = BoardUser(user=request.user, permission='owner', board=board)
            board_user.save()
            messages.success(request, "Board created successfully.")
            return redirect('boards:edit', id = board.reference)

@login_required
def edit(request, id):
    if request.method == 'GET':
        board = Board.objects.get(reference=id)
        try:
            version = BoardVersion.objects.filter(board_id=board.id).latest('id')
        except BoardVersion.DoesNotExist:
            version = BoardVersion(content="", board=board, modified_by=request.user)
            version.save()
        return render(request, "boards/edit.html", {'board': board, 'version': version})
    elif request.method == 'POST':
        c = Crypto()
        board = Board.objects.get(reference=id)
        content = c.encrypt(request.POST.get("content"))
        version = BoardVersion(content=content, board=board, modified_by=request.user)
        version.save()
        messages.success(request, f"Changes on the board saved successfully.")
        return redirect('boards:show', id = board.reference)

@login_required
def share(request, id):
    if request.method == 'GET':
        board = Board.objects.get(reference=id)
        existing_user_ids = BoardUser.objects.filter(board_id=board.id).values_list('user_id', flat=True)
        data_for_options = User.objects.all().exclude(id__in=existing_user_ids).values_list('id', 'first_name', 'last_name')
        return render(request, "boards/share.html", {'board': board, 'data_for_options': data_for_options})
    elif request.method == 'POST':
        board = Board.objects.get(reference=id)
        user_id = bleach.clean(request.POST.get("user_id"))
        user = User.objects.get(pk=user_id)
        permission = bleach.clean(request.POST.get("permission"))
        board_user = BoardUser(board=board, user_id=user_id, permission=permission)
        board_user.save()
        messages.success(request, f"Board shared with {user.get_full_name()} successfully.")
        return redirect('boards:show', id = board.reference)

@login_required
def versions(request, id):
    board = Board.objects.get(reference=id)
    versions = board.versions().order_by('-created_at')
    return render(request, "boards/versions.html", {'board': board, 'versions': versions})

@login_required
def restore_version(request, version_id):
    version = BoardVersion.objects.get(pk=version_id)
    c = Crypto()
    new_version = BoardVersion(content=c.encrypt(version.content), board=version.board, modified_by=request.user)
    new_version.save()
    messages.success(request, "Board version restored successfully.")
    return redirect('boards:show', id = new_version.board.reference)
