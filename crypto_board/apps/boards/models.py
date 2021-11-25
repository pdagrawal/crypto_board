from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.RESTRICT)
    reference = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def owner_name(self):
        return (self.owner.first_name + ' ' + self.owner.last_name)

    def board_title(self):
        return self.name[:20]

class BoardVersion(models.Model):
    content = models.TextField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.board.name

    def content_snippet(self):
        return self.content[:50]
