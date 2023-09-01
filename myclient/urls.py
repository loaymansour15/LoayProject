"""DjangoApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .views import MyLogoutView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.home, name='homeURL'),

    #authentication
    path('login/', views.login_view, name='loginURL'),
    path('logout/', MyLogoutView.as_view(), name='logout'),

    #product in store
    path('add_product/', views.add_product, name='addProduct'),
    path('add_product_setting/', views.add_product_setting, name='addProductSetting'),

    #add order
    path('add_order_client_detail/', views.add_order_client_details, name='addOrderClientDetail'),
    path('add_order_product_detail/', views.add_order_product_details, name='addOrderProductDetail'),

    #path('get_variants/', views.get_product_variants, name='getVariants'),

    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name="resetPassword"),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),),
    path('accounts/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_completed.html'),),
]
