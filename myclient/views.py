from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

class MyLogoutView(LogoutView):
    next_page = '/login/'

def home(request):
    return HttpResponse("Hello, world. You're at the polls index.")