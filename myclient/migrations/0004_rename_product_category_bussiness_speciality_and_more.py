# Generated by Django 4.1 on 2023-08-25 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myclient', '0003_alter_brandprofile_business_user_name_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product_Category',
            new_name='Bussiness_Speciality',
        ),
        migrations.RemoveField(
            model_name='brandprofile',
            name='product_category',
        ),
    ]