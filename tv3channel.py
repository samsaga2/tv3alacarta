import xbmc
import tv3
from menu import MenuItem, Menu
from channel import Channel
    

class TV3Channel(Channel):
    def build_episodes_menu(self, episodes, include_subtitle=False):
        menu = Menu(self.base_url, self.addon_handle)
        for item in episodes:
            if include_subtitle and len(item.subtitle) != 0:
                title = '{0} - {1}'.format(item.title, item.subtitle)
            else:
                title = item.title
            video = {"Title": title, "Plot": item.plot, "Date": item.date}
            li = MenuItem(title, 'play', args={'code': item.code}, iconImage='DefaultVideo.png', video=video)
            menu.add(li)
        menu.show()         
    
    
    def mode__mainmenu(self):
        menu = Menu(self.base_url, self.addon_handle)
        menu.add(MenuItem('Programes', 'programes', iconImage='DefaultFolder.png'))
        menu.add(MenuItem('Directe', 'directe', iconImage='DefaultFolder.png'))
        menu.add(MenuItem('Mes destacats', 'mesdestacats', iconImage='DefaultFolder.png'))
        menu.add(MenuItem('Mes vistos', 'mesvistos', iconImage='DefaultFolder.png'))
        menu.add(MenuItem('Mes votats', 'mesvotats', iconImage='DefaultFolder.png'))
        menu.show()
        
        
    def mode__directe(self):
        menu = Menu(self.base_url, self.addon_handle)
        menu.add(MenuItem('TV3', 'arafem', args={'canal': 'TV3'}, iconImage='DefaultVideo.png'))
        menu.add(MenuItem('TV3 CAT', 'arafem', args={'canal': 'TV3CAT'}, iconImage='DefaultVideo.png'))
        menu.add(MenuItem('C33', 'arafem', args={'canal': '33'}, iconImage='DefaultVideo.png'))
        menu.add(MenuItem('3/24', 'arafem', args={'canal': '324'}, iconImage='DefaultVideo.png'))
        menu.add(MenuItem('Super 3', 'arafem', args={'canal': 'SUPER3'}, iconImage='DefaultVideo.png'))
        menu.add(MenuItem('Cameres TV3', 'arafem', args={'canal': 'cameres'}, iconImage='DefaultVideo.png'))
        menu.show()
        
        
    def mode__mesdestacats(self):
        shows = tv3.get_mesdestacats()
        self.build_episodes_menu(shows, True)
    
    
    def mode__mesvotats(self):
        shows = tv3.get_mesvotats()
        self.build_episodes_menu(shows, True)
    
    
    def mode__mesvistos(self):
        shows = tv3.get_mesvistos()
        self.build_episodes_menu(shows, True)
        
    
    def mode__programes(self):
        menu = Menu(self.base_url, self.addon_handle)
        for letter in tv3.letters:
            li = MenuItem(letter, 'letter', args={'letter': letter}, iconImage='DefaultFolder.png')
            menu.add(li)
        menu.show() 
    
    
    def mode__letter(self):
        letter = self.args['letter'][0]
        menu = Menu(self.base_url, self.addon_handle)
        for show in tv3.get_letter(letter):
            iconImage = show.img if len(show.img) > 0 else 'DefaultVideo.png'
            li = MenuItem(show.title, 'episodes', args={'code': show.code}, iconImage=iconImage)
            menu.add(li)
        menu.show() 
        
        
    def mode__episodes(self):
        code = self.args['code'][0]
        episodes = tv3.get_episodes(code)
        self.build_episodes_menu(episodes)
        
        
    def mode__arafem(self):
        canal = self.args['canal'][0]
        rtmp = tv3.get_canal_stream(canal)
        xbmc.Player().play(rtmp)
        
    
    def mode__play(self):
        code = self.args['code'][0]
        videos = tv3.get_media(code)
        video = videos[0]
        rtmp = tv3.get_show_rtmp(code, video.quality_code, video.format)
        xbmc.Player().play(rtmp)
