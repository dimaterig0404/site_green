# Generated by Django 3.2.12 on 2022-06-03 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0042_auto_20220603_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_all_seanses',
            name='ident_key',
            field=models.CharField(default='lgAFmXOwrtYdkIn', max_length=20, verbose_name='Специальный код сеанса'),
        ),
        migrations.AlterField(
            model_name='data_all_seanses',
            name='summa',
            field=models.IntegerField(default=817, verbose_name='Цена билета'),
        ),
    ]
