# Generated by Django 2.2 on 2019-04-11 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Новая', 'Новая'), ('Выполняется', 'Выполняется'), ('Закрыта', 'Закрыта'), ('Отклонена', 'Отклонена'), ('Дубликат', 'Дубликат')], default='Новая', max_length=64, verbose_name='Статус')),
                ('priority', models.CharField(choices=[('Срочная', 'Срочная'), ('Обычная', 'Обычная')], default='Обычная', max_length=64, verbose_name='Приоритет')),
                ('request_type', models.CharField(blank=True, choices=[('Электрооборудование', 'Электрооборудование'), ('Сантехника', 'Сантехника'), ('Прочее', 'Прочее')], default='Прочее', max_length=255, null=True, verbose_name='Тип поломки')),
                ('closed_on', models.DateField()),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Создана')),
                ('is_proceed', models.BooleanField(default=False)),
                ('assigned_to', models.ManyToManyField(blank=True, related_name='request_assigned_staff', to='accounts.Account')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
