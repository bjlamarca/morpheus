

class Capability():
    def On(self, state):
        print(state)


class HueDeviceTypes():
    #
    def __init__(self):
        self.device_list = [
            {
                'display_name': 'White Light',
                'hue_device_type': 'WHITELAMP',
                'morph_name': 'HUEWHITELAMP',
                'morph_display_name': 'Hue White Light',
                'capability': 'switch, dimmer',
                'morph_sync': True

            },
            {
                'display_name': 'Color Light',
                'hue_name': 'COLORLAMP',
                'morph_name': 'HUECOLORLAMP',
                'morph_display_name': 'Hue Color Light',
                'capability': 'color, switch, dimmer',
                'morph_sync': True

            },
            {
                'display_name': 'Dimmer Switch',
                'hue_name': 'DIMSWITCH',
                'morph_name': 'HUEDIMSWITCH',
                'morph_display_name': 'Hue Dimmer Switch',
                'morph_sync': False

            },
            {
                'display_name': 'Hub',
                'hue_name': 'HUB',
                'morph_name': 'HUEHUB',
                'morph_display_name': 'Hue Hub',
                'morph_sync': False

            },
            
        ]
    def get_device_list(self):
        return self.device_list
            