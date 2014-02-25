import xbmc
import a3media
from menu import MenuItem, Menu
from channel import Channel
    

class A3MediaChannel(Channel):
    def mainmenu(self):
        menu = Menu(self.base_url, self.addon_handle)
        for item in a3media.get_mainmenu():
            menu.add(MenuItem(item['title'], 'section', args={'id': item['id']}, iconImage=item['img']))
        menu.show()
        
        
    def mode__section(self):
        id = self.args['id'][0]
        menu = Menu(self.base_url, self.addon_handle)
        for item in a3media.get_section(id):
            video = {"Plot": item['plot']}
            menu.add(MenuItem(item['title'], 'subcategories', args={'id': id, 'subid': item['id']}, iconImage=item['img'], video=video))
        menu.show()


    def mode__subcategories(self):
        id = self.args['id'][0]
        subid = self.args['subid'][0]
        menu = Menu(self.base_url, self.addon_handle)
        for item in a3media.get_subcategories(id, subid):
            video = {"Plot": item['plot']}
            menu.add(MenuItem(item['title'], 'episodes', args={'id': item['id']}, iconImage=item['img'], video=video))
        menu.show()

        
    def mode__episodes(self):
        id = self.args['id'][0]
        menu = Menu(self.base_url, self.addon_handle)
        for item in a3media.get_episodes(id):
            video = {"Plot": item['plot']}
            menu.add(MenuItem(item['title'], 'play', args={'id': id}, iconImage=item['img'], video=video))
        menu.show()


    def mode__play(self):
        # TODO https://github.com/aabilio/PyDownTV2/blob/master/spaintvs/grupo_a3.py:488
        pass
