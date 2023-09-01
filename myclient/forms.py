from django import forms

from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import *

def check_arabic_no(str_num):
    to_en = ""
    ar_arr = "٠١٢٣٤٥٦٧٨٩"
    en_arr = "0123456789"

    for i in str_num:
        ind = ar_arr.find(i)
        if ind > -1:
            en_no = en_arr[ind]
        else:
            en_no = i
        to_en = to_en + en_no

    return to_en

def has_nums(str_char):
    found = False
    ar_arr = "٠١٢٣٤٥٦٧٨٩"
    en_arr = "0123456789"

    for i in str_char:
        ind_ar = ar_arr.find(i)
        ind_en = en_arr.find(i)
        if ind_ar > -1 or ind_en > -1:
            found = True
            break
    return found

def has_char(str_mobile):
    found = False

    for i in str_mobile:
        okay = i.isdigit()
        if not okay:
            found = True
            break
    return found

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control text-right','placeholder': 'إسم البراند'}))
    #email = forms.EmailField(max_length=150, required=True, widget=forms.EmailInput(attrs={'class': 'form-control text-right','placeholder': ' البريد الإلكتروني '}))
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control text-right','placeholder': 'كلمة المرور'}))

    #def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        #for key, field in self.fields.items():
            #field.label = ""
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = 'إسم البراند '
        self.fields['password'].label = 'كلمة المرور'

class AddProductUnit_Form(forms.ModelForm):
    class Meta:
        model = Product_Unit
        exclude = ('user',)
        widgets = {
            'name_unit': forms.TextInput(attrs={ 'placeholder':'مثال: كيلو , قطعة , متر '}),
        }

class AddProductVariant_Form(forms.ModelForm):
    class Meta:
        model = Product_Variant
        exclude = ('user',)
        widgets = {
            'name_var': forms.TextInput(attrs={ 'placeholder':'مثال: لون , مقاس '}),
        }


class AddProductVariantOptions_Form(forms.ModelForm):
    class Meta:
        model = Product_Variant_Options
        fields = "__all__"
        widgets = {
            'name_var_op': forms.TextInput(attrs={ 'placeholder':'مثال: في حالة اللون (احمر ، ازرق ) '}),
        }

class AddProductCategory_Form(forms.ModelForm):
    class Meta:
        model = Product_Category
        exclude = ('user',)
        widgets = {
            'name_cat': forms.TextInput(attrs={ 'placeholder':' فئة المنتج '}),
        }

class AddProduct_Form(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('user',)


'''
class User_Type_Choice_Form(forms.ModelForm):
    class Meta:
        model = User_Type_Choice
        fields = '__all__'
        

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label="كلمة السر")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="إعادة كلمة السر")

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                "كلمة المرور غير مطابقة"
            )

class Info_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class BrandProfileForm(forms.ModelForm):

    class Meta:
        model = BrandProfile
        exclude = ('user', 'approved_by_admin')
        widgets = {
            'mobile1_has_whatsapp': forms.CheckboxInput(attrs={ 'style':'margin-right: 80px;'}),
            'mobile2_has_whatsapp': forms.CheckboxInput(attrs={ 'style':'margin-right: 80px;'}),

        }
    
    def clean(self):
        self.cleaned_data = super(BrandProfileForm, self).clean()
        mobile1 = self.cleaned_data['mobile1']
        mobile2 = self.cleaned_data['mobile2']
        mobile2_has_whatsapp = self.cleaned_data['mobile2_has_whatsapp']
        business_user_name = self.cleaned_data['business_user_name']

        if mobile1 and has_char(mobile1):
            self.add_error('mobile1',"  يجب ان لا يتكون رقم الموبايل من اي حرف  ")
        if mobile1 and len(mobile1) != 11:
            self.add_error('mobile1',"يجب أن يتكون رقم الموبايل من 11 رقمًا")
        if mobile2 and has_char(mobile2):
            self.add_error('mobile2',"  يجب ان لا يتكون رقم الموبايل من اي حرف  ")
        if mobile2 and len(mobile2) != 11:
            self.add_error('mobile2',"يجب أن يتكون رقم الموبايل من 11 رقمًا")
        if not mobile2 and mobile2_has_whatsapp:
            self.add_error('mobile2_has_whatsapp', ' لا يمكن اضافه واتس اب لرقم موبايل 2 لانه غير موجود ')
        if mobile1 and mobile2 and mobile1 == mobile2:
            self.add_error('mobile2', ' يجب تغيير موبايل رقم 2 ليصبح مختلف عن موبايل رقم 1 ')

        if mobile1:
            self.cleaned_data['mobile1'] = check_arabic_no(mobile1)
        if mobile2:
            self.cleaned_data['mobile2'] = check_arabic_no(mobile2)
        
        if business_user_name and has_nums(business_user_name):
            self.add_error('business_user_name',"  يجب ان لا يتكون الإسم من اي رقم عربي او انجليزي ")

        if business_user_name and len(business_user_name) < 2:
            self.add_error('business_user_name',"  الإسم غير كامل")
        
        return self.cleaned_data
    

class Privacy_Accept(forms.Form):
    priv_check_box = forms.CharField(max_length=150, required=True, widget=forms.CheckboxInput(attrs={ 'style':'margin-right: 0px;'}))

    def __init__(self, *args, **kwargs):
        super(Privacy_Accept, self).__init__(*args, **kwargs)

        self.fields['priv_check_box'].label = ' أوافق علي شروط الخصوصية  '

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='أدخل عنوان بريد إلكتروني ', label="بريد إلكتروني")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '  '}),
        }
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = 'إسم الشركة '

        validator = RegexValidator(r'^[a-zA-Z0-9]*$', 'مطلوب. 150 رمزاً أو أقل، مكونة من حروف وأرقام فقط ')
        self.fields['username'].validators = [validator]
        self.fields['username'].help_text = 'أدخل إسم الشركة    '

        #   مطلوب. 150 رمزاً أو أقل، مكونة من حروف وأرقام فقط   

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control text-right','placeholder': 'إسم الشركة'}))
    #email = forms.EmailField(max_length=150, required=True, widget=forms.EmailInput(attrs={'class': 'form-control text-right','placeholder': ' البريد الإلكتروني '}))
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control text-right','placeholder': 'كلمة المرور'}))

    #def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        #for key, field in self.fields.items():
            #field.label = ""
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = 'إسم الشركة '
        self.fields['password'].label = 'كلمة المرور'


# i score forms
class Search_for_Client_Form(forms.Form):
    mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'رقم الموبايل', 'maxlength':'11'}), required=True, label="")

    def clean(self):
        mobile = self.cleaned_data['mobile']
        st = mobile.find("01", 0, 2) 
        if mobile and st == -1:
            self.add_error('mobile',"  يجب ان يبدء الرقم ب 01  ")
        if mobile and len(mobile) != 11:
            self.add_error('mobile',"يجب أن يتكون رقم الهاتف المحمول من 11 رقمًا")
        if mobile and has_char(mobile):
            self.add_error('mobile',"  يجب ان لا يتكون رقم الموبايل من احرف  ")
        
        

class Add_Client_Form(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '*إسم العميل بالكامل'}),
            'mobileNo1': forms.TextInput(attrs={'class': 'form-control text-right', 'placeholder': '*1 رقم الموبايل'}),
            'mobileNo2': forms.TextInput(attrs={'class': 'form-control text-right', 'placeholder': '2 رقم الموبايل'}),
            'mobileNo3': forms.TextInput(attrs={'class': 'form-control text-right', 'placeholder': '3 رقم الموبايل'}),
            
        }

    def clean(self):
        self.cleaned_data = super(Add_Client_Form, self).clean()
        name = self.cleaned_data['name']
        mobileNo1 = self.cleaned_data['mobileNo1']
        mobileNo2 = self.cleaned_data['mobileNo2']
        mobileNo3 = self.cleaned_data['mobileNo3']

        
        
        
        if mobileNo1 :
            st = mobileNo1.find("01", 0, 2) 
            if st == -1:
                self.add_error('mobileNo1',"  يجب ان يبدء الرقم ب 01  ")
        
        if mobileNo2 :
            st1 = mobileNo2.find("01", 0, 2) 
            if st1 == -1:
                self.add_error('mobileNo2',"  يجب ان يبدء الرقم ب 01  ")
        
        if mobileNo3 :
            st2 = mobileNo3.find("01", 0, 2) 
            if st2 == -1:
                self.add_error('mobileNo3',"  يجب ان يبدء الرقم ب 01  ")

        if name and has_nums(name):
            self.add_error('name',"  يجب ان لا يتكون الإسم من رقم عربي او انجليزي ")
        if name and len(name) < 2:
            self.add_error('name',"  الإسم غير كامل")
        if mobileNo1 and has_char(mobileNo1):
            self.add_error('mobileNo1',"  يجب ان لا يتكون رقم الموبايل من احرف  ")
        if mobileNo2 and has_char(mobileNo2):
            self.add_error('mobileNo2',"  يجب ان لا يتكون رقم الموبايل من احرف  ")
        if mobileNo3 and has_char(mobileNo3):
            self.add_error('mobileNo3',"  يجب ان لا يتكون رقم الموبايل من احرف  ")
        if mobileNo1 and mobileNo2 and mobileNo1 == mobileNo2:
            self.add_error('mobileNo1',' يجب تغيير موبايل رقم 1 ليصبح مختلف عن موبايل رقم 2 ')
        if mobileNo1 and mobileNo3 and mobileNo1 == mobileNo3:
            self.add_error('mobileNo3',' يجب تغيير موبايل رقم 3 ليصبح مختلف عن موبايل رقم 1 ')
        if mobileNo2 and mobileNo3 and mobileNo2 == mobileNo3:
            self.add_error('mobileNo2',' يجب تغيير موبايل رقم 2 ليصبح مختلف عن موبايل رقم 3 ')
        if mobileNo1:
            self.cleaned_data['mobileNo1'] = check_arabic_no(mobileNo1)
        if mobileNo2:
            self.cleaned_data['mobileNo2'] = check_arabic_no(mobileNo2)
        if mobileNo3:
            self.cleaned_data['mobileNo3'] = check_arabic_no(mobileNo3)
        if mobileNo1 and len(mobileNo1) != 11:
            self.add_error('mobileNo1',"يجب أن يتكون رقم الموبايل من 11 رقمًا")
        if mobileNo2 and len(mobileNo2) != 11:
            self.add_error('mobileNo2',"يجب أن يتكون رقم الموبايل من 11 رقمًا")
        if mobileNo3 and len(mobileNo3) != 11:
            self.add_error('mobileNo3',"يجب أن يتكون رقم الموبايل من 11 رقمًا")

        return self.cleaned_data


class Report_Tag_Form(forms.ModelForm):
    class Meta:
        model = Report
        fields = ("report_tag",)


class Recharge_Form(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control text-right','placeholder': 'إسم الشركة'}))
    
    def __init__(self, *args, **kwargs):
        super(Recharge_Form, self).__init__(*args, **kwargs)

        self.fields['username'].label = 'إسم الشركة '

'''