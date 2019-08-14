from django.db import models

# Create your models here.
class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    exchange_id = models.CharField(max_length=255,null=True,blank=True)
    event_start = models.DateTimeField(null=True,blank=True)
    event_end = models.DateTimeField(null=True,blank=True)
    event_subject = models.CharField(max_length=255,null=True,blank=True)
    event_location = models.CharField(max_length=255,null=True,blank=True)
    event_category = models.CharField(max_length=255,null=True,blank=True)
    event_attendees = models.CharField(max_length=255,null=True,blank=True)