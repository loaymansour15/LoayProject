# Generated by Django 4.1 on 2023-09-01 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myclient', '0012_product_category_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_category',
            old_name='name',
            new_name='name_cat',
        ),
        migrations.RenameField(
            model_name='product_unit',
            old_name='name',
            new_name='name_unit',
        ),
        migrations.RenameField(
            model_name='product_variant',
            old_name='name',
            new_name='name_var',
        ),
        migrations.RenameField(
            model_name='product_variant_options',
            old_name='name',
            new_name='name_var_op',
        ),
    ]
