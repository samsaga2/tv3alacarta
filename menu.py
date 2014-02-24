import xbmcgui
import xbmcplugin
import urllib


class MenuItem:
    def __init__(self, title, mode, args={}, iconImage=None, video=None):
        self.title = title
        self.mode = mode
        self.args = args
        self.iconImage = iconImage
        self.video = video
        
    def url(self, base_url):
        query = dict([('mode', self.mode)] + self.args.items())
        url = base_url + '?' + urllib.urlencode(query)
        return url

    def add(self, base_url):
        url = self.url(base_url)
        li = xbmcgui.ListItem(self.title, iconImage=self.iconImage)
        if self.video:
            li.setInfo('Video', self.video)
        return url, li
    
        
class Menu:
    def __init__(self, base_url, addon_handle):
        self.base_url = base_url
        self.addon_handle = addon_handle
        self.items = []
        
    def add(self, item):
        self.items.append(item)

    def build_url(self, query):
        return self.base_url + '?' + urllib.urlencode(query)
        
    def show(self):
        for item in self.items:
            url, li = item.add(self.base_url)
            xbmcplugin.addDirectoryItem(handle=self.addon_handle, url=url, listitem=li, isFolder=True)
        xbmcplugin.endOfDirectory(self.addon_handle)
