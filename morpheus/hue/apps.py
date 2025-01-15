from django.apps import AppConfig


class HueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hue'

    def ready(self):
        import hue.signals
        from .hub import Hub
        hub = Hub()
        hub.set_hub(1)
        hub.hue_receive_events() 