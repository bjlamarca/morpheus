from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class DeviceType(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name'
    )
    display_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Display Name'
    )
    interface_device_type = models.CharField(
        max_length=100,
        verbose_name='Interface Display Name'
    )
    interface = models.CharField(
        max_length=100,
        verbose_name='Interface'
    )
    capability = models.CharField(
        max_length=500,
        verbose_name='Capabilities'
    )

    def __str__(self):
        return self.display_name

    def get_absolute_url(self):
        return reverse('devices:devicetype', args=[self.pk])


class Device(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name'
    )

    device_content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Content Type'
    )
    device_object_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name='Content Object ID'
    )

    device_content_object = GenericForeignKey(
        'device_content_type',
        'device_object_id',
    
        
    )
    device_type = models.ForeignKey(
        DeviceType,
        on_delete = models.CASCADE,
        verbose_name='Device Type'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('devices:device-detail', args=[self.pk])


