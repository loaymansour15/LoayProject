# Generated by Django 4.1 on 2023-08-25 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myclient', '0008_alter_product_unit_alter_product_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_unit',
            name='name',
            field=models.CharField(max_length=100, verbose_name='إضافة وحدة جديدة'),
        ),
        migrations.CreateModel(
            name='Product_Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='إضافة نوع متغير جديد')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]