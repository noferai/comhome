# Generated by Django 2.2.2 on 2019-07-25 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeowners', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeowner',
            name='apartments',
            field=models.ManyToManyField(blank=True, null=True, to='apartments.Apartment'),
        ),
    ]
