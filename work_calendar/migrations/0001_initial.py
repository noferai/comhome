# Generated by Django 2.2.6 on 2019-10-25 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('exchange_id', models.CharField(blank=True, max_length=255, null=True)),
                ('event_start', models.DateTimeField(blank=True, null=True)),
                ('event_end', models.DateTimeField(blank=True, null=True)),
                ('event_subject', models.CharField(blank=True, max_length=255, null=True)),
                ('event_location', models.CharField(blank=True, max_length=255, null=True)),
                ('event_category', models.CharField(blank=True, max_length=255, null=True)),
                ('event_attendees', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
