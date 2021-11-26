import uuid
from django.db import models
from django.contrib.auth.models import User
from mirage.crypto import Crypto

class Board(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    reference = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def owner_name(self):
        return self.owner.get_full_name()

    def decrypted_name(self):
        c = Crypto()
        return c.decrypt(self.name)

    def latest_content(self):
        version = BoardVersion.objects.filter(board_id=self.id).latest('id')
        if version is not None:
            return version.decrypted_content()
        else:
            return ''

    def set_reference_number(self):
        reference_number = uuid.uuid4()
        if Board.objects.filter(reference=reference_number).exists():
            self.set_reference_number()
        else:
            self.reference = reference_number
            return self

    def versions(self):
        return BoardVersion.objects.filter(board_id=self.id)

class BoardVersion(models.Model):
    content = models.TextField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.board.name

    def modified_by_name(self):
        return self.modified_by.get_full_name()

    def decrypted_content(self):
        c = Crypto()
        return c.decrypt(self.content)

class BoardUser(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.board.name}:{self.user.get_full_name()}"