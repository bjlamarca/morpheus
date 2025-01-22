from utilities.logging import SystemLogger


logger = SystemLogger('tiles', __name__)

class PageTypes():
    def __init__(self):
        self.page_type_list = [
            {
                'name': 'standard',
                'display_name': 'Standard',
            },
            {
                'name': 'home',
                'display_name': 'Home'
            },
            
        ]

    def get_page_types_choices(self):
        return_list = []
        for page_dict in self.page_type_list:
            page_tuple = (page_dict['name'], page_dict['display_name'])
            return_list.append(page_tuple)

        return return_list


class TileTypes():
    def __init__(self):
        self.tile_type_list = [
            {
                'name': 'scene',
                'display_name': 'Scene'
            },
            {
                'name': 'nav',
                'display_name': 'Navigation',
            },
            
        ]

    def get_tile_types_choices(self):
        return_list = []
        for tile_dict in self.tile_type_list:
            tile_tuple = (tile_dict['name'], tile_dict['display_name'])
            return_list.append(tile_tuple)

        print(return_list)




    
    