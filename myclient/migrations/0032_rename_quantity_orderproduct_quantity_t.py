# Generated by Django 4.1 on 2023-09-09 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myclient', '0031_alter_orderproduct_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='quantity',
            new_name='quantity_t',
        ),
    ]
