# Generated by Django 4.1 on 2023-08-30 17:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myclient', '0004_remove_product_variant_remove_product_variant_option_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cost',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000000)], verbose_name='التكلفة'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='variant1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='v1', to='myclient.product_variant', verbose_name='  نوع المتغير 1 '),
        ),
        migrations.AlterField(
            model_name='product',
            name='variant2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='v2', to='myclient.product_variant', verbose_name='  نوع المتغير 2 '),
        ),
        migrations.AlterField(
            model_name='product',
            name='variant_option1',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=' إضافة إسم متغير 1 '),
        ),
        migrations.AlterField(
            model_name='product',
            name='variant_option2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=' إضافة إسم متغير 2 '),
        ),
    ]