# Generated by Django 2.2.2 on 2019-06-30 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0003_apartment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='business_account',
            field=models.CharField(max_length=500, verbose_name='Лицевой счет'),
        ),
    ]