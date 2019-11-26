# Generated by Django 2.2.6 on 2019-10-25 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apartments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Группа услуг')),
                ('accrued', models.FloatField(verbose_name='Начислено')),
                ('paid', models.FloatField(verbose_name='Оплачено')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Создано')),
                ('modified_on', models.DateField(auto_now=True, verbose_name='Изменено')),
                ('apartment', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='apartments.Apartment')),
            ],
            options={
                'verbose_name': 'Взаиморасчет',
                'verbose_name_plural': 'Взаиморасчеты',
                'ordering': ['created_on'],
            },
        ),
    ]