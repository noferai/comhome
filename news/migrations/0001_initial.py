# Generated by Django 2.2.6 on 2019-10-25 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2000, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('status', models.BooleanField(choices=[(True, 'Опубликовано'), (False, 'Черновик')], default=False, verbose_name='Статус')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Создано')),
                ('modified_on', models.DateField(auto_now=True, verbose_name='Изменено')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['created_on'],
            },
        ),
    ]
