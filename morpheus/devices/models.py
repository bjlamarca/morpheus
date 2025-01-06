from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class DeviceType(models.Model):
    name = models.CharField(
        max_length=100
    )
    display_name = models.CharField(
        max_length=100,
        blank=True
    )
    interface_device_type = models.CharField(
        max_length=100
    )
    interface = models.CharField(
        max_length=100
    )
    capability = models.CharField(
        max_length=500
    )



class Device(models.Model):
    name = models.CharField(
        max_length=100
    )

    device_content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    device_object_id = models.PositiveBigIntegerField(
        null=True,
        blank=True
    )

    device_content_object = GenericForeignKey(
        'device_content_type',
        'device_object_id'
    )
    device_type = models.ForeignKey(
        DeviceType,
        on_delete = models.CASCADE,
        verbose_name='Device Type'
    )


