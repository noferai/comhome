# Generated by Django 2.2.6 on 2019-10-30 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_staff_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='occupation',
            field=models.CharField(choices=[('Не указано', 'Не указано'), ('Электрик', 'Электрик'), ('Сантехник', 'Сантехник'), ('Слесарь', 'Слесарь'), ('Слаботочник', 'Слаботочник'), ('Охранник', 'Охранник')], default='Не указано', max_length=255, verbose_name='Тип деятельности'),
        ),
    ]
