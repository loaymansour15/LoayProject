# Generated by Django 4.1 on 2023-09-01 15:36

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('myclient', '0013_rename_name_product_category_name_cat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_unit',
            name='name_unit',
            field=models.CharField(max_length=100, verbose_name='إضافة وحدة جديدة'),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=100, verbose_name='إسم العميل ')),
                ('mobile1', models.CharField(max_length=11, null=True, verbose_name='موبايل 1')),
                ('mobile1_has_whatsapp', models.BooleanField(default=True, verbose_name=' واتس اب ؟')),
                ('mobile2', models.CharField(blank=True, max_length=11, null=True, verbose_name='موبايل 2')),
                ('mobile2_has_whatsapp', models.BooleanField(default=False, verbose_name=' واتس اب ؟')),
                ('address', models.CharField(max_length=200, verbose_name='العنوان تفصيلي  ')),
                ('country_c', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myclient.country', verbose_name='الدولة')),
                ('state_c', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='country_c', chained_model_field='country', null=True, on_delete=django.db.models.deletion.CASCADE, to='myclient.state', verbose_name='المحافظة')),
            ],
        ),
    ]
