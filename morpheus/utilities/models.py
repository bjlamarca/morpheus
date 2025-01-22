from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType


class SystemLog(models.Model):
    date_time = models.DateTimeField()
    content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Content Type'
    )
    module = models.CharField(
        max_length=100,
        blank=True,
        null=True
    ) 
    method = models.CharField(
        max_length=100,
        blank=True
    )
    message = models.CharField(
        max_length=3000

    )
    details = models.CharField(
        max_length=3000
    )
    level = models.CharField(
        max_length=20
    )

    class Meta:
        verbose_name = 'System Log'

    def __str__(self):
        return str(self.date_time)

    def get_absolute_url(self):
        return reverse('ultilities:systemlog', args=[self.pk])
