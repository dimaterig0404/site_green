# Generated by Django 3.2.12 on 2022-06-06 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp2', '0042_auto_20220606_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_all_seanses',
            name='ident_key',
            field=models.CharField(default='xeUJmvhoBdWzaHN', max_length=20, verbose_name='Специальный код сеанса'),
        ),
        migrations.AlterField(
            model_name='data_all_seanses',
            name='summa',
            field=models.IntegerField(default=243, verbose_name='Цена билета'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sopose',
            field=models.CharField(blank=True, max_length=5, verbose_name='Qr, 18, med'),
        ),
    ]
