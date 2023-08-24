# Generated by Django 4.1 on 2023-08-24 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myclient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_link', models.CharField(blank=True, max_length=100, null=True, verbose_name=' لينك الويب سايت')),
                ('scoial_link', models.CharField(max_length=80, null=True, verbose_name=' لينك السوشيال ميديا الرئيسية')),
                ('business_user_name', models.CharField(max_length=100, null=True, verbose_name='اسم الشخص المسئول')),
                ('mobile1', models.CharField(max_length=11, null=True, verbose_name='موبايل 1')),
                ('mobile1_has_whatsapp', models.BooleanField(default=True, verbose_name=' واتس اب ؟')),
                ('mobile2', models.CharField(blank=True, max_length=11, null=True, verbose_name='موبايل 2')),
                ('mobile2_has_whatsapp', models.BooleanField(default=False, verbose_name=' واتس اب ؟')),
                ('approved_by_admin', models.BooleanField(default=False, verbose_name='  الحساب مفعل؟ ')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')),
                ('country_c', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myclient.country', verbose_name='الدولة')),
                ('product_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myclient.product_category', verbose_name='  فئة منتجاتك')),
                ('state_c', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='country_c', chained_model_field='country', null=True, on_delete=django.db.models.deletion.CASCADE, to='myclient.state', verbose_name='المحافظة')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
