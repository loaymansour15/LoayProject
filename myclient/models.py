from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.


User._meta.get_field('email')._unique = True


class Country(models.Model):
    name = models.CharField(max_length=50)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name


class Bussiness_Speciality(models.Model):
    name = models.CharField(max_length=100)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name


class BrandProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website_link = models.CharField(max_length=100, verbose_name=" لينك الويب سايت", blank=True, null=True)
    scoial_link = models.CharField(max_length=80, verbose_name=" لينك السوشيال ميديا الرئيسية", blank=True, null=True)
    business_speciality = models.ForeignKey("Bussiness_Speciality", on_delete=models.CASCADE, verbose_name="  تخصص البراند ", blank=True, null=True)
    #est_no_of_orders_per_month = models.IntegerField(verbose_name="تقريبا كم عدد الأوردرات في الشهر", validators=[MinValueValidator(0),MaxValueValidator(100000)])
    country_c = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="الدولة", blank=True, null=True)
    state_c = ChainedForeignKey(State, chained_field="country_c", chained_model_field="country", show_all=False, auto_choose=True, sort=True, verbose_name="المحافظة", blank=True, null=True)
    #city_c = ChainedForeignKey(City, chained_field="state_c", chained_model_field="state", show_all=False, auto_choose=True, sort=True, verbose_name="المدينه", blank=True, null=True)
    business_user_name = models.CharField(max_length=100, verbose_name="اسم الشخص المسئول", blank=True, null=True)
    mobile1 = models.CharField(max_length=11, verbose_name="موبايل 1", blank=True, null=True)
    mobile1_has_whatsapp = models.BooleanField(default=True, verbose_name=" واتس اب ؟")
    mobile2 = models.CharField(max_length=11, blank=True, null=True, verbose_name="موبايل 2")
    mobile2_has_whatsapp = models.BooleanField(default=False, verbose_name=" واتس اب ؟")
    approved_by_admin = models.BooleanField(default=False, verbose_name="  الحساب مفعل؟ ")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    #class Meta:
        #constraints = [
             #models.UniqueConstraint(fields=['mobile1', 'mobile2'], name='unique_number1'),
        #]

    def __str__(self):
        return self.user.username

class Product_Unit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="إضافة وحدة جديدة")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name

class Product_Variant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="إضافة نوع متغير جديد")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name


class Product_Variant_Options(models.Model):
    prod_variant = models.ForeignKey("Product_Variant", on_delete=models.CASCADE, verbose_name="نوع المتغير")
    name = models.CharField(max_length=100, verbose_name="إضافة متغير جديد")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="إسم المنتج")
    unit = models.ForeignKey("Product_Unit", on_delete=models.CASCADE, verbose_name="الوحدة")
    variant = models.ForeignKey("Product_Variant", on_delete=models.CASCADE, verbose_name="نوع المتغير", blank=True, null=True)
    variant_option = ChainedForeignKey(Product_Variant_Options, chained_field="variant", chained_model_field="prod_variant", show_all=False, auto_choose=True, sort=True, verbose_name="إسم المتغير", blank=True, null=True)
    quantity = models.IntegerField(verbose_name="الكمية", validators=[MinValueValidator(0),MaxValueValidator(10000000)])

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name