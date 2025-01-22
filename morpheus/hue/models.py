from django.db import models
from django.urls import reverse



HUE_DEVICE_TYPE = [
        ['WHITELAMP', 'White Lamp'],
        ['COLORLAMP', 'Color Lamp'],
        ['DIMSWITCH', 'Dimmer Switch'],
        ['HUB', 'Hue Hub']
    ]

class HueDevice(models.Model):
    #Morpheus categorization of Hue devices  
    hue_device_type = models.CharField(
        max_length=100,
        blank=True,
        choices=HUE_DEVICE_TYPE,
        verbose_name='Hue Device Type'
    )
    hub_id = models.IntegerField(
        blank=False,
        verbose_name='Hub ID'
    )
    hue_id = models.CharField(
        max_length=100,
        verbose_name='Hue ID'
    )
    hue_id_v1 = models.CharField(
        max_length=100
    )
    model_id = models.CharField(
        max_length=100,
        verbose_name='Model ID'
    )
    manufacturer_name = models.CharField(
        max_length=100,
        verbose_name='Manufacture Name'
    )
    product_name = models.CharField(
        max_length=100,
        verbose_name='Product Name'

    )
    software_version = models.CharField(
        max_length=100,
        verbose_name='Software Version'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Name'

    )
    zigbee_rid = models.CharField(
        max_length=100,
        verbose_name='ZigBee RID'

    )
    power_rid = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Power RID'
    )
    bridge_rid = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Bridge RID'
    )
    online = models.BooleanField(
        blank=True,
        null=True,
        default=True,
        verbose_name='Online'
    )
    last_checkin = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Last Check-in'
        
    )
    battery_level = models.IntegerField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Battery Level'
    )
    morph_sync = models.BooleanField(  
        default=False,
        verbose_name='Sync to Devices'
    )
    class Meta:
        verbose_name = 'Hue Device'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hue:device', args=[self.pk])

SWITCH_CHOICES = [
    ['on', 'On'],
    ['off', 'Off']
]

class HueLight(models.Model):
    
    device = models.ForeignKey(
        HueDevice,
        on_delete = models.CASCADE,
        verbose_name='Device'
    )
    rid = models.CharField(
        max_length=100,
        verbose_name='RID'
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
    gamut_type = models.CharField(max_length=50,
        blank=True,
        null=True,
        verbose_name='Gamut Type'
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
    effect = models.CharField(max_length=50,
        blank=True,
        null=True,
        verbose_name='Effect'
    )

    class Meta:
        verbose_name = 'Hue Light'

    def __str__(self):
        return self.rid

    def get_absolute_url(self):
        return reverse('hue:light', args=[self.pk])
        
class HueButton(models.Model):
    device = models.ForeignKey(
        HueDevice,
        on_delete = models.CASCADE,
        verbose_name='Device'
    )
    rid = models.CharField(
        max_length=100,
        verbose_name='RID'
    )
    name = models.CharField(
        max_length=300,
        verbose_name='Name'
    )
    updated = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Last Update'
    )
    event = models.CharField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Last Event'
    )
    

    class Meta:
        verbose_name = 'Hue Buttons'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hue:light', args=[self.pk])
