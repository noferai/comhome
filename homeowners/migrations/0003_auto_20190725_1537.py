# Generated by Django 2.2.2 on 2019-07-25 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeowners', '0002_auto_20190725_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeowner',
            name='apartments',
            field=models.ManyToManyField(blank=True, null=True, related_name='owners', to='apartments.Apartment'),
        ),
    ]
