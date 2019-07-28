# Generated by Django 2.2.3 on 2019-07-28 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apartments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='apartment_created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
