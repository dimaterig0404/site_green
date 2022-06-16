# Generated by Django 3.2.12 on 2022-05-22 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20220521_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_all_seanses',
            name='ident_key',
            field=models.CharField(default='bPLthoABfTmIusn', max_length=20, verbose_name='Специальный код сеанса'),
        ),
        migrations.AlterField(
            model_name='data_all_seanses',
            name='summa',
            field=models.IntegerField(default=299, verbose_name='Цена билета'),
        ),
    ]
