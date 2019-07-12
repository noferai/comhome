# Generated by Django 2.2.2 on 2019-07-12 21:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apartment_number', models.PositiveSmallIntegerField(verbose_name='Номер квартиры')),
                ('entrance', models.PositiveSmallIntegerField(verbose_name='Подъезд')),
                ('floor', models.PositiveSmallIntegerField(verbose_name='Этаж')),
                ('number_of_rooms', models.PositiveSmallIntegerField(verbose_name='Количество комнат')),
                ('area', models.FloatField(blank=True, null=True, verbose_name='Площадь')),
                ('business_account', models.CharField(max_length=500, verbose_name='Лицевой счет')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('Не заселена', 'Не заселена'), ('Заселена', 'Заселена')], default='Не заселена', max_length=64, verbose_name='Статус')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalog.Address')),
            ],
        ),
    ]