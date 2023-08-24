from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
import pyarabic.araby as araby
import pyarabic.number as number
from django.db.models import Q

# Create your views here.


# Login / Logout / Register / Other functions related to login to user authentication

class MyLogoutView(LogoutView):
    next_page = '/login/'

def login_view(request):
    if request.user.is_authenticated:
        return redirect('homeURL')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            usr = User.objects.filter(username=username).first()

            # username is found in database
            if usr:

                #create a brand & wallet model
                has_brand = BrandProfile.objects.filter(user=usr).first()
                if not has_brand:
                    new_brand = BrandProfile(user=usr)
                    new_brand.save()

                # user is approved to use our website
                brand_is_approved = BrandProfile.objects.filter(Q(user=usr), Q(approved_by_admin=True)).filter()
                if brand_is_approved:

                    # username and password matches a record in database
                    user_is_auth = authenticate(request, username=username, password=password)
                    if user_is_auth is not None: 
                        login(request, usr)
                        messages.success(request, f' {username}! اهلا')
                        return redirect('homeURL')
                    else:
                        messages.error(request, 'اسم المستخدم او كلمة السر قد تكون خطأ')
                else:
                    messages.error(request, '  حسابك غير مفعل ')
            else:
                messages.error(request, '  لا يوجد حساب بهذا الإسم')

        else:
            messages.error(request, ' برجاء إضافه البيانات بشكل صحيح ')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'login.html', context)


def home(request):

    context = {}
    return render(request, 'home.html', context)