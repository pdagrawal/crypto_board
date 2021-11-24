from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def index(request):
    return render(request, "boards/index.html")

def show(request, id):
    return render(request, "boards/show.html")

def edit(request, id):
    return render(request, "boards/edit.html")
