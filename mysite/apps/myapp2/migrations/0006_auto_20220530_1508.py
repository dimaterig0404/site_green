# Generated by Django 3.2.12 on 2022-05-30 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp2', '0005_auto_20220529_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_all_seanses',
            name='ident_key',
            field=models.CharField(default='SpwHmVJUEoZFjRQ', max_length=20, verbose_name='Специальный код сеанса'),
        ),
        migrations.AlterField(
            model_name='data_all_seanses',
            name='summa',
            field=models.IntegerField(default=415, verbose_name='Цена билета'),
        ),
    ]
