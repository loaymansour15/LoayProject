# Generated by Django 4.1 on 2023-09-10 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myclient', '0034_alter_brandcourierprices_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brandcourierprices',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myclient.state', verbose_name='المحافظة'),
        ),
    ]
