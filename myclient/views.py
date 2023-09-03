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

import random
import math

from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
#import pyarabic.araby as araby
#import pyarabic.number as number
from django.db.models import Q
import json
from django.http import JsonResponse, request
import random
from datetime import date, datetime, timezone


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


# Store Functions
@login_required
def add_product(request):

    if request.method == 'POST':
        form = AddProduct_Form(request.POST)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.user = request.user
            newForm.save()

            messages.success(request, 'تم تسجيل المنتج بنجاح')
            return redirect('addProduct')
        else:
            messages.error(request, ' برجاء إضافه البيانات بشكل صحيح ')
    else: # GET
        form = AddProduct_Form()
    
    context = {'form':form}

    return render(request, 'add_product.html', context)


@login_required
def add_product_setting(request):
    if request.method == 'POST':
        form1 = AddProductUnit_Form(request.POST)
        form2 = AddProductVariant_Form(request.POST)
        form3 = AddProductVariantOptions_Form(request.POST)
        form4 = AddProductCategory_Form(request.POST)
        if request.POST['action'] == "frm1":
            if form1.is_valid():
                name_unit = form1.cleaned_data.get('name_unit')
                found = Product_Unit.objects.filter(user=request.user, name_unit=name_unit).first()
                if not found:
                    newForm1 = form1.save(commit=False)
                    newForm1.user = request.user
                    newForm1.save()
                    messages.success(request, 'تم تسجيل الوحدة بنجاح')
                else:
                    messages.error(request, 'تم تسجيل الوحدة مسبقا')
                return redirect('addProductSetting')

        if request.POST['action'] == "frm2":
            if form2.is_valid():
                name_var = form2.cleaned_data.get('name_var')
                found = Product_Variant.objects.filter(user=request.user, name_var=name_var).first()
                if not found:
                    newForm2 = form2.save(commit=False)
                    newForm2.user = request.user
                    newForm2.save()
                    messages.success(request, 'تم تسجيل نوع المتغير بنجاح')
                else:
                    messages.error(request, 'تم تسجيل نوع المتغير مسبقا')
                return redirect('addProductSetting')

        if request.POST['action'] == "frm3":
            if form3.is_valid():
                prod_variant = form3.cleaned_data.get('prod_variant')
                name_var_op = form3.cleaned_data.get('name_var_op')
                found = Product_Variant_Options.objects.filter(prod_variant=prod_variant, name_var_op=name_var_op).first()
                if not found:
                    form3.save()
                    messages.success(request, 'تم تسجيل إسم المتغير بنجاح')
                else:
                    messages.error(request, 'تم تسجيل إسم المتغير مسبقا')
                return redirect('addProductSetting')

        if request.POST['action'] == "frm4":
            if form4.is_valid():
                name_cat = form4.cleaned_data.get('name_cat')
                found = Product_Category.objects.filter(user=request.user, name_cat=name_cat).first()
                if not found:
                    newForm4 = form4.save(commit=False)
                    newForm4.user = request.user
                    newForm4.save()
                    messages.success(request, 'تم تسجيل فئة المنتج بنجاح')
                else:
                    messages.error(request, 'تم تسجيل فئة المنتج مسبقا')
                return redirect('addProductSetting')
        else:
            messages.error(request, ' برجاء إضافه البيانات بشكل صحيح ')
    else: # GET
        form1 = AddProductUnit_Form()
        form2 = AddProductVariant_Form()
        form3 = AddProductVariantOptions_Form()
        form4 = AddProductCategory_Form()
    
    context = {'form1':form1, 'form2':form2, 'form3':form3, 'form4':form4}

    return render(request, 'product_setting.html', context)

@login_required
def start_order(request):
    if request.method == 'POST':
        while True:
            order_uid = generate_order_uid()
            found = Order.objects.filter(order_uid=order_uid).first()
            if not found:
                new_order = Order(order_uid=order_uid, user=request.user)
                new_order.save()
                break

        return redirect('addOrderProductDetail', ouid=order_uid)
    else:
        return render(request, 'start_order.html')


def generate_order_uid():
    digits = [i for i in range(0, 10)]
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    ## initializing a string
    random_str = ""

    for i in range(2):
        ## generating a random index
        ## if we multiply with 10 it will generate a number between 0 and 10 not including 10
        ## multiply the random.random() with length of your base list or str
        index = math.floor(random.random() * 26)
        random_str += alpha[index]

    ## we can generate any lenght of string we want
    for i in range(7):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])


    return random_str


@login_required
def add_order_product_details(request, ouid):

    if request.method == 'POST':
        p_id = request.POST.get('product')
        product = Product.objects.filter(id=p_id).first()
        if product:
            pass
            #save the product in order product
            messages.success(request, 'تم حفظ المنتج بنجاح')
            return redirect('addOrderProductDetail', ouid)

    form = AddOrderProductDetail_Form()
    
    context = {'form':form, 'ouid':ouid}

    return render(request, 'order_product_detail.html', context)

#ajax function get_product_data
@login_required
def get_product_data(request):
    
    prod = request.GET.get('prod_id')
    prod_id = json.loads(prod)
    p = Product.objects.filter(id=prod_id).first()
    result = []
    result.append((p.unit.id, p.quantity, p.cost, p.price, p.discount, p.variant1.id, p.variant_option1.id, p.variant2.id, p.variant_option2.id))
        
    data = {'result': result}
    return JsonResponse((data))

@login_required
def add_order_shipping_details(request, ouid):

    form = AddOrderShippingDetail_Form()
    
    context = {'form':form, 'ouid':ouid}

    return render(request, 'order_shipping_detail.html', context)

@login_required
def add_order_client_details(request, ouid):

    form = AddOrderClientDetail_Form()
    
    context = {'form':form, 'ouid':ouid}

    return render(request, 'order_client_detail.html', context)

@login_required
def delete_order(request, ouid):

    found = Order.objects.filter(user=request.user, order_uid=ouid).first()
    if found:
        found.delete()
        # delete from all releated tables
        messages.success(request, 'تم إلغاء الطلب بنجاح')
    else:
        messages.error(request, 'هناك خطأ أثناء إلغاء الطلب')

    return redirect('startOrder')


#ajax
@login_required
def add_product_unit(request):

    if request.method == 'POST':
        form = AddProductUnit_Form(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')

            new_unit = Product_Unit.objects.filter(name=name, user=request.user).first()
            exist = None
            if not new_unit:
                new_unit = Product_Unit(name=name, user=request.user)
                new_unit.save()
                exist = False
            else:
                exist = True
                
                #messages.success(request, f'{name}! تم إضافه الوحده ')
                #messages.error(request, f'   {name}! تم إضافتها مسبقا ')
        
            data = {'p_unit': name, 'exist':exist, 'option_text':new_unit.name, 'option_value':new_unit.id}
            return JsonResponse(data)


@login_required
def add_product_variant(request):
    if request.method == 'POST':
        form = AddProductVariant_Form(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')

            new_variant = Product_Variant.objects.filter(name=name, user=request.user).first()
            exist = None
            if not new_variant:
                new_variant = Product_Variant(name=name, user=request.user)
                new_variant.save()
                exist = False
            else:
                exist = True
                
                #messages.success(request, f'{name}! تم إضافه الوحده ')
                #messages.error(request, f'   {name}! تم إضافتها مسبقا ')
        
            data = {'p_variant': name, 'exist':exist, 'option_text':new_variant.name, 'option_value':new_variant.id}
            return JsonResponse(data)

'''
@login_required
def add_product_var_options(request):
    if request.method == 'POST':
        form = AddProductVariantOptions_Form(request.POST)
        if form.is_valid():
            prod_variant = form.cleaned_data.get('prod_variant')
            name = form.cleaned_data.get('name')
            prod_var = Product_Variant.objects.filter(user=request.user, name=prod_variant).first()
            if prod_var:
                new_var_option = Product_Variant_Options.objects.filter(name=name, prod_variant=prod_var).first()
                exist = None
                if not new_var_option:
                    new_var_option = Product_Variant_Options(name=name, prod_variant=prod_var)
                    new_var_option.save()
                    exist = False
                else:
                    exist = True
            
                data = {'p_variant': name, 'exist':exist, 'option_text':new_var_option.name, 'option_value':new_var_option.id}
                return JsonResponse(data)
            else:
                pass
'''

@login_required
def get_product_variants(request):
    all_variants = Product_Variant.objects.all()
    result = []
    for a in all_variants:
        result.append((a.id, a.name))
        
    data = {'variants': result}
    return JsonResponse(data)

