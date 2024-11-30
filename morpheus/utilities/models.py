from django.db import models
from django.urls import reverse


class SystemLog(models.Model):
    date_time = models.DateTimeField()
    area = models.CharField(
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
