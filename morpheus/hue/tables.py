import django_tables2 as tables
from .models import Device

class DeviceTable(tables.Table):
    class Meta:
        model = Device
        