# Generated by Django 4.1 on 2023-09-01 16:47

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('myclient', '0017_orderproduct_date_created_orderproduct_date_modified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='variant1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vp1', to='myclient.product_variant', verbose_name='  نوع المتغير 1 '),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variant2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vp2', to='myclient.product_variant', verbose_name='  نوع المتغير 2 '),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variant_option1',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='variant1', chained_model_field='prod_variant', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vrp1', to='myclient.product_variant_options', verbose_name=' إسم متغير 1 '),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variant_option2',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='variant2', chained_model_field='prod_variant', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vrp2', to='myclient.product_variant_options', verbose_name=' إسم متغير 2 '),
        ),
    ]
