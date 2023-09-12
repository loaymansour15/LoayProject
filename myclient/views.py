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
    if request.user.is_authenticated:
        pass
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
    while True:
        order_uid = generate_order_uid()
        found = Order.objects.filter(order_uid=order_uid).first()
        if not found:
            new_order = Order(order_uid=order_uid, user=request.user)
            new_order.save()
            break

    return redirect('showAllProducts', ouid=order_uid)


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
def show_all_products(request, ouid):

    products = Product.objects.filter(user=request.user).all()
    
    context = {'products':products, 'ouid':ouid, 'link': 'addOrderProductDetail'}

    return render(request, 'order_show_all_user_prods.html', context)

@login_required
def show_all_order_products(request, ouid):

    found_order = Order.objects.filter(order_uid=ouid, user=request.user).first()
    products = OrderProduct.objects.filter(order=found_order).all()
    
    context = {'products':products, 'ouid':ouid, 'link': 'addOrderProductDetail'}

    return render(request, 'order_products.html', context)

@login_required
def add_order_product_details(request, ouid, id):

    product = Product.objects.filter(id=id).first()
    this_order = Order.objects.filter(order_uid=ouid, user=request.user).first()
    order_product = OrderProduct.objects.filter(order=this_order, product=product).first()
    if request.method == 'POST':
        if order_product:#if order product is already here
            form = AddOrderProductDetail_Form(request.POST, instance=order_product)
            if form.is_valid():
                quantity = form.cleaned_data.get('quantity_t')
                cost = form.cleaned_data.get('cost')
                price = form.cleaned_data.get('price')
                discount = form.cleaned_data.get('discount')
                if int(quantity) > 0 and int(price) > 0 and int(cost) > 0:
                    if product:
                        order_product2 = OrderProduct.objects.filter(order=this_order, product=product).first()
                        temp_all_quant = product.quantity + order_product2.quantity_t
                        print(temp_all_quant, quantity, order_product2.quantity_t, 'helloooooo')
                        if int(quantity) > temp_all_quant:
                            messages.error(request, 'الكميه غير متوفرة في المخزن')
                            return render(request, 'order_product_detail.html', {'form':form, 'ouid':ouid, 'id':id})
                        else:
                            #save the product in order product
                            orderProduct = OrderProduct.objects.filter(order=this_order).update(category=product.category, product=product, unit=product.unit, quantity_t=quantity, price=price, cost=cost, discount=discount, variant1=product.variant1, variant_option1=product.variant_option1, variant2=product.variant2, variant_option2=product.variant_option2)
                            product.quantity = int(temp_all_quant) - int(quantity)
                            product.save()
                            messages.success(request, 'تم حفظ المنتج بنجاح')
                            return redirect('showAllProducts', ouid=ouid)
                else:
                    messages.error(request, 'يجب ان لا يكون الكميه والسعر والتكلفه = 0')
            else:
                messages.error(request, 'لم يتم العثور علي المنتج')
                return redirect('showAllProducts', ouid=ouid)
        else:#if order product is not added to cart
            form = AddOrderProductDetail_Form(request.POST)
            if form.is_valid():
                quantity = form.cleaned_data.get('quantity_t')
                cost = form.cleaned_data.get('cost')
                price = form.cleaned_data.get('price')
                discount = form.cleaned_data.get('discount')
                found_order = Order.objects.filter(order_uid=ouid, user=request.user).first()
                found_prod_in_order = OrderProduct.objects.filter(order=found_order, product=product).first()
                if not found_prod_in_order:
                    if int(quantity) > 0 and int(price) > 0 and int(cost) > 0:
                        if product:
                            if int(quantity) > product.quantity:
                                messages.error(request, 'الكميه غير متوفرة في المخزن')
                                return render(request, 'order_product_detail.html', {'form':form, 'ouid':ouid, 'id':id})
                            else:
                                #save the product in order product
                                this_order = Order.objects.filter(order_uid=ouid, user=request.user).first()
                                orderProduct = OrderProduct(order=this_order, category=product.category, product=product, unit=product.unit, quantity_t=quantity, price=price, cost=cost, discount=discount, variant1=product.variant1, variant_option1=product.variant_option1, variant2=product.variant2, variant_option2=product.variant_option2)
                                orderProduct.save()
                                product.quantity = product.quantity - int(quantity)
                                product.save()
                                messages.success(request, 'تم حفظ المنتج بنجاح')
                                return redirect('showAllProducts', ouid=ouid)
                    else:
                        messages.error(request, 'يجب ان لا يكون الكميه والسعر والتكلفه = 0')
                else:
                    messages.error(request, 'تم إضافه المنتج مسبقا لهذا الطلب')
            else:
                messages.error(request, 'لم يتم العثور علي المنتج')
                return redirect('showAllProducts', ouid=ouid)
    else:#GET
        
        if order_product:#if order product is already here
            form = AddOrderProductDetail_Form(instance=order_product)
        else:
            form = AddOrderProductDetail_Form(instance=product)
    context = {'form':form, 'ouid':ouid, 'id':id}

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

    this_order = Order.objects.filter(order_uid=ouid, user=request.user).first()
    order_shipp_detail = OrderShippingDetail.objects.filter(order=this_order).first()
    if request.method == 'POST':
        if this_order and not order_shipp_detail:# add for first time
            form = AddOrderShippingDetail_Form(request.POST)
            if form.is_valid():
                cost = form.cleaned_data.get('cost')
                free_shipping = form.cleaned_data.get('free_shipping')
                state = form.cleaned_data.get('state')
                if (free_shipping and cost == 0) or (not free_shipping and cost > 0):
                    new_form = form.save(commit=False)
                    new_form.order = this_order
                    new_form.save()
                    curr_state = State.objects.filter(name=state).first()
                    order_client_detail = OrderClient(order=this_order, state=curr_state)
                    order_client_detail.save()
                    messages.success(request, 'تم تسجيل بيانات الشحن بنجاح')
                elif free_shipping and cost > 0:
                    messages.error(request, 'في حاله تكلفة الشحن المجاني يجب أن تكون تكلفة الشحن صفر')
                elif not free_shipping and cost == 0:
                    messages.error(request, 'في حاله تكلفة الشحن الغير مجاني يجب أن تكون تكلفة الشحن أكبر من صفر')
        elif this_order and order_shipp_detail:# already added before and want to edit
            form = AddOrderShippingDetail_Form(request.POST, instance=order_shipp_detail)
            if form.is_valid():
                cost = form.cleaned_data.get('cost')
                free_shipping = form.cleaned_data.get('free_shipping')
                state = form.cleaned_data.get('state')
                if (free_shipping and cost == 0) or (not free_shipping and cost > 0):
                    new_form = form.save(commit=False)
                    new_form.order = this_order
                    new_form.save()
                    curr_state = State.objects.filter(name=state).first()
                    order_client_detail = OrderClient.objects.filter(order=this_order).first()
                    order_client_detail.state = curr_state
                    order_client_detail.save()
                    messages.success(request, 'تم تسجيل بيانات الشحن بنجاح')
                elif free_shipping and cost > 0:
                    messages.error(request, 'في حاله تكلفة الشحن المجاني يجب أن تكون تكلفة الشحن صفر')
                elif not free_shipping and cost == 0:
                    messages.error(request, 'في حاله تكلفة الشحن الغير مجاني يجب أن تكون تكلفة الشحن أكبر من صفر')
        else:
            messages.error(request, 'هذا الطلب اصبح غير موجود')
    else:#GET
        if order_shipp_detail:
            form = AddOrderShippingDetail_Form(instance=order_shipp_detail)
        else:
            form = AddOrderShippingDetail_Form()

    context = {'form':form, 'ouid':ouid}

    return render(request, 'order_shipping_detail.html', context)


def add_order_client_details(request, ouid):

    this_order = Order.objects.filter(order_uid=ouid).first()
    order_client_detail = OrderClient.objects.filter(order=this_order).first()
    if request.method == 'POST':
        if not order_client_detail:
            form = AddOrderClientDetail_Form(request.POST)
            form2 = AddOrderClientDetail_State_Form()
            messages.error(request, 'بيانات الشحن غير مكتمله')
        else:
            form = AddOrderClientDetail_Form(request.POST, instance=order_client_detail)
            form2 = AddOrderClientDetail_State_Form(instance=order_client_detail)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.state = order_client_detail.state
                new_form.save()
                messages.success(request, 'تم تسجيل بيانات العميل بنجاح')
    else:#GET
        if order_client_detail:
            form = AddOrderClientDetail_Form(instance=order_client_detail)
            form2 = AddOrderClientDetail_State_Form(instance=order_client_detail)
        else:
            form = AddOrderClientDetail_Form()
            form2 = AddOrderClientDetail_State_Form()
    
    context = {'form':form, 'ouid':ouid, 'form2': form2}

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

    return redirect('allOrders')


@login_required
def all_orders(request):
    orders = Order.objects.filter(user=request.user).all()
    context = {'orders': orders, 'link':'showAllProducts'}
    return render(request, 'all_orders.html', context)

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


@login_required
def get_courier_shipping_cost(request):
    courier = request.GET.get('courier')
    courier_id = json.loads(courier)

    state = request.GET.get('state')
    state_id = json.loads(state)

    courier_id = Courier.objects.filter(id=int(courier_id)).first()
    state_id = State.objects.filter(id=int(state_id)).first()
    brand_cour_prices = BrandCourierPrices.objects.filter(user=request.user, courier=courier_id, state=state_id).first()
    print(brand_cour_prices, 'heloooo')

    result = ""
    if brand_cour_prices:
        result = str(brand_cour_prices.cost) +" جم "+ "تكلفة الشحن" + " " + " لمحافظة " + " " + state_id.name + " " + " مع " + " " + courier_id.courier_name + " "
    else:
        result =   "لا توجد تكلفة شحن" + " " + " لمحافظة " + " " + state_id.name + " " + " مع " + " " + courier_id.courier_name + " "

    data = {'result': result}
    return JsonResponse((data))