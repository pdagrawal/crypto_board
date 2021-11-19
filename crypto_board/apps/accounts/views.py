import bleach
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages

from crypto_board import settings

from .forms import SignupForm

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        form = SignupForm()
    elif request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = bleach.clean(form.cleaned_data["username"])
            first_name = bleach.clean(form.cleaned_data["first_name"])
            last_name = bleach.clean(form.cleaned_data["last_name"])
            email = bleach.clean(form.cleaned_data["email"])
            password = bleach.clean(form.cleaned_data["password"])
            confirm_password = bleach.clean(form.cleaned_data["confirm_password"])

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, "Your account has been successfully created.")
            send_mail(f"Welcome to CryptoBoard!", "Signup email content", settings.DEFAULT_FROM_EMAIL, [email])
            return redirect('accounts:login')
    else:
        raise NotImplementedError
    return render(request, "accounts/signup.html", {"form": form})