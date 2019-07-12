# Generated by Django 2.2.2 on 2019-07-12 21:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Новая', 'Новая'), ('Выполняется', 'Выполняется'), ('Закрыта', 'Закрыта'), ('Отклонена', 'Отклонена'), ('Дубликат', 'Дубликат')], default='Новая', max_length=64, verbose_name='Статус')),
                ('priority', models.CharField(choices=[('Срочная', 'Срочная'), ('Обычная', 'Обычная')], default='Обычная', max_length=64, verbose_name='Приоритет')),
                ('request_type', models.CharField(blank=True, choices=[('Электрооборудование', 'Электрооборудование'), ('Сантехника', 'Сантехника'), ('Уборщик', 'Уборщик'), ('Прочее', 'Прочее')], default='Прочее', max_length=255, null=True, verbose_name='Тип поломки')),
                ('closed_on', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Создана')),
                ('is_proceed', models.BooleanField(default=False)),
                ('assigned_to', models.ManyToManyField(blank=True, related_name='request_assigned_staff', to='staff.Staff')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]