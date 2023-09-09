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
    #country = models.ForeignKey(Country, on_delete=models.CASCADE)

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
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name="المحافظة", blank=True, null=True)
    #state_c = ChainedForeignKey(State, chained_field="country_c", chained_model_field="country", show_all=False, auto_choose=True, sort=True, verbose_name="المحافظة", blank=True, null=True)
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
    name_unit = models.CharField(max_length=100, verbose_name="إضافة وحدة جديدة")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name_unit

class Product_Variant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_var = models.CharField(max_length=100, verbose_name="إضافة نوع متغير جديد")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name_var

class Product_Variant_Options(models.Model):
    prod_variant = models.ForeignKey("Product_Variant", on_delete=models.CASCADE, verbose_name="نوع المتغير")
    name_var_op = models.CharField(max_length=100, verbose_name="إضافة إسم متغير جديد")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name_var_op

class Product_Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name_cat = models.CharField(max_length=100, verbose_name="فئة المنتج")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name_cat

'''
class Product_Variant_Dynamic_Options(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name="المنتج")
    variant = models.ForeignKey("Product_Variant", on_delete=models.CASCADE, verbose_name="نوع المتغير", blank=True, null=True)
    variant_option = models.CharField(max_length=100, verbose_name="إضافة إسم متغير ", blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.product
'''

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="إسم المنتج")
    category = models.ForeignKey("Product_Category", on_delete=models.CASCADE, verbose_name="فئة المنتج", null=True)
    unit = models.ForeignKey("Product_Unit", on_delete=models.CASCADE, verbose_name="الوحدة")
    quantity = models.IntegerField(verbose_name="الكمية", validators=[MinValueValidator(0),MaxValueValidator(10000000)], default=0)
    cost = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(10000000)], verbose_name="التكلفة", default=0)
    price = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(10000000)], verbose_name="سعر البيع  ", default=0)
    discount = models.IntegerField( validators=[MinValueValidator(0),MaxValueValidator(10000000)], verbose_name="الخصم  ", default=0, blank=True)
    variant1 = models.ForeignKey("Product_Variant", on_delete=models.CASCADE, verbose_name="  نوع المتغير 1 ", blank=True, null=True, related_name="v1")
    variant_option1 = ChainedForeignKey(Product_Variant_Options, chained_field="variant1", chained_model_field="prod_variant", show_all=False, auto_choose=True, sort=True, verbose_name=" إسم متغير 1 ", blank=True, null=True, related_name="vr1")
    variant2 = models.ForeignKey("Product_Variant", on_delete=models.CASCADE, verbose_name="  نوع المتغير 2 ", blank=True, null=True, related_name="v2")
    variant_option2 = ChainedForeignKey(Product_Variant_Options, chained_field="variant2", chained_model_field="prod_variant", show_all=False, auto_choose=True, sort=True, verbose_name=" إسم متغير 2 ", blank=True, null=True, related_name="vr2")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey("Client", on_delete=models.CASCADE, null=True)
    order_uid = models.CharField(max_length=500, verbose_name="رقم الأوردر ", unique=True)
    total_order_before_shipp = models.CharField(max_length=500, verbose_name="إجمالي الطلب قبل الشحن", null=True)
    total_order_after_shipp = models.CharField(max_length=500, verbose_name="إجمالي الطلب شامل الشحن", null=True)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.order_uid


class OrderProduct(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    category = models.ForeignKey("Product_Category", on_delete=models.CASCADE, verbose_name="فئة المنتج", null=True)
    product = ChainedForeignKey("Product", chained_field="category", chained_model_field="category", show_all=False, auto_choose=False, sort=True, verbose_name=" إسم المنتج  ", blank=False, null=True)
    unit = models.ForeignKey("Product_Unit", on_delete=models.CASCADE, verbose_name="الوحدة ", null=True)
    quantity_t = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(10000000)], verbose_name="الكمية", default=0)
    cost = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(10000000)], verbose_name="التكلفة", default=0)
    price = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(10000000)], verbose_name="سعر البيع ", default=0)
    discount = models.IntegerField( validators=[MinValueValidator(0),MaxValueValidator(10000000)], verbose_name="الخصم ", default=0, blank=True)
    variant1 = models.ForeignKey("Product_Variant", on_delete=models.CASCADE, verbose_name="  نوع المتغير 1 ", blank=True, null=True, related_name="vp1")
    variant_option1 = models.ForeignKey("Product_Variant_Options", on_delete=models.CASCADE, verbose_name=" إسم متغير 1 ", blank=True, null=True, related_name="vpo1")
    variant2 = models.ForeignKey("Product_Variant", on_delete=models.CASCADE, verbose_name="  نوع المتغير 2 ", blank=True, null=True, related_name="vp2")
    variant_option2 = models.ForeignKey("Product_Variant_Options", on_delete=models.CASCADE, verbose_name=" إسم متغير 2 ", blank=True, null=True, related_name="vpo2")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.order.order_uid

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    client_name = models.CharField(max_length=100, verbose_name="إسم العميل ")
    mobile1 = models.CharField(max_length=11, verbose_name="موبايل 1", blank=False, null=True)
    mobile1_has_whatsapp = models.BooleanField(default=True, verbose_name=" واتس اب ؟")
    mobile2 = models.CharField(max_length=11, blank=True, null=True, verbose_name="موبايل 2")
    mobile2_has_whatsapp = models.BooleanField(default=False, verbose_name=" واتس اب ؟")
    address = models.CharField(max_length=200, verbose_name="العنوان تفصيلي  ")
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name="المحافظة", blank=False, null=True)
    
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.client_name


class Courier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    courier_name = models.CharField(max_length=100, verbose_name="إسم شركة الشحن ")
    person_name = models.CharField(max_length=100, verbose_name="إسم مسئول شركة الشحن ")
    mobile1 = models.CharField(max_length=11, verbose_name="موبايل المسئول", blank=False, null=True)
    mobile1_has_whatsapp = models.BooleanField(default=True, verbose_name=" واتس اب ؟")
    
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.courier_name


class BrandCourierPrices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courier = models.ForeignKey("Courier", on_delete=models.CASCADE, verbose_name="إسم شركة الشحن ")
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name="المحافظة", blank=False, null=True)
    cost = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(10000000)], verbose_name="التكلفة", default=0)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    def __str__(self):
        return self.courier