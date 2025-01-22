from django.db import models
from devices.models import Device
from django.urls import reverse
# Create your models here.

class Scene(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('scenes:detail', args=[self.pk])

SWITCH_CHOICES = [
    ['on', 'On'],
    ['off', 'Off']
] 

class SceneDevices(models.Model):
    
    scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        verbose_name='Device'
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        verbose_name='Device'
    )
    scene_device_capability = models.CharField(
        max_length=500,
        verbose_name='Capabilities',
        blank=True,
        null=True,
    )
    light_on = models.BooleanField(
        blank=True,
        null=True,
        verbose_name='Light On'
    )
    switch = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=SWITCH_CHOICES,
        verbose_name='Switch'
    )
    dimming = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Dimming'
        )
    red = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Red'
        )
    green = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Green'
        )
    blue = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Blue'
        )
    
 
    


