# Generated by Django 2.2.3 on 2019-07-28 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2000, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('published_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
    ]
