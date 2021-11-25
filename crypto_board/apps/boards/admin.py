from django.contrib import admin

from .models import Board, BoardVersion, BoardUser

admin.site.register(Board)
admin.site.register(BoardVersion)
admin.site.register(BoardUser)
