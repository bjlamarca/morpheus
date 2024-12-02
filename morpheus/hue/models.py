from django.db import models
from django.urls import reverse


class Device(models.Model):
    #Morpheus categorization of Hue devices  
    hue_device_type = models.CharField(
        max_length=100,
        blank=True
    )
    hub_id = models.IntegerField(
        blank=False,
    )
    hue_id = models.CharField(
        max_length=100
    )
    hue_id_v1 = models.CharField(
        max_length=100
    )
    model_id = models.CharField(
        max_length=100
    )
    manufacturer_name = models.CharField(
        max_length=100
    )
    product_name = models.CharField(
        max_length=100
    )
    software_version = models.CharField(
        max_length=100
    )
    name = models.CharField(
        max_length=100
    )
    zigbee_rid = models.CharField(
        max_length=100
    )
    power_rid = models.CharField(
        max_length=100,
        blank=True
    )
    bridge_rid = models.CharField(
        max_length=100,
        blank=True
    )
    last_checkin = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        
    )

    class Meta:
        verbose_name = 'Hue Device'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hue:device', args=[self.pk])

class Light(models.Model):
    
    device = models.ForeignKey(
        Device,
        on_delete = models.CASCADE
    )
    rid = models.CharField(
        max_length=100
    )
    light_on = models.BooleanField(
        blank=True,
        null=True
    )
    dimming = models.IntegerField(
        blank=True,
        null=True
        )
    gamut_type = models.CharField(max_length=50,
        blank=True,
        null=True
        )
    red = models.IntegerField(blank=True, null=True)
    green = models.IntegerField(blank=True, null=True)
    blue = models.IntegerField(blank=True, null=True)
    effect = models.CharField(max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Hue Light'

    def __str__(self):
        return self.rid

    def get_absolute_url(self):
        return reverse('hue:light', args=[self.pk])
        
class Button(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete = models.CASCADE
    )
    rid = models.CharField(
        max_length=100
    )
    name = models.CharField(
        max_length=300
    )

    class Meta:
        verbose_name = 'Hue Buttons'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hue:light', args=[self.pk])
