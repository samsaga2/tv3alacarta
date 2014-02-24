# URL INFO http://www.tv3.cat/pvideo/FLV_bbd_dadesItem.jsp?idint=4705751
# URL RTMP http://www.tv3.cat/pvideo/FLV_bbd_media.jsp?PROFILE=EVP&ID=4705751&QUALITY=H&FORMAT=MP4
#    el QUALITY y el FORMAT salen del URL INFO

'''
REMOTE_DBG = True 
if REMOTE_DBG:
    try:
        import pysrc.pydevd as pydevd
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)
'''        

import xbmc
import xbmcgui
import xbmcplugin
import urlparse
import urllib
import tv3


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
 
xbmcplugin.setContent(addon_handle, 'movies')


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
    

def build_episodes_menu(episodes, include_subtitle=False):
    for episode in episodes:
        if include_subtitle and len(episode.subtitle) != 0:
            title = '{0} - {1}'.format(episode.title, episode.subtitle)
        else:
            title = episode.title
        url = build_url({'mode': 'play', 'code': episode.code})
        li = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=episode.img)
        li.setInfo("Video", {"Title": title, "Plot": episode.plot, "Date": episode.date})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True) 
    xbmcplugin.endOfDirectory(addon_handle)


def menu_mainmenu():
    items = [{'title': 'Programes', 'mode':'programes'},
             {'title': 'Directe', 'mode':'directe'},
             {'title': 'Mes destacats', 'mode':'mesdestacats'},
             {'title': 'Mes vistos', 'mode':'mesvistes'},
             {'title': 'Mes votats', 'mode':'mesvotats'},
             ]    
    for item in items:
        url = build_url({'mode': item['mode']})
        li = xbmcgui.ListItem(item['title'], iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
    
    
def menu_directe():
    items = [{'title': 'TV3', 'canal':'TV3'},
             {'title': 'TV3 CAT', 'canal':'TV3CAT'},
             {'title': 'C33', 'canal':'33'},
             {'title': '3/24', 'canal':'324'},
             {'title': 'Super 3', 'canal':'SUPER3'},
             {'title': 'Cameres TV3', 'canal':'cameres'}
             ]
    for item in items:
        url = build_url({'mode': 'arafem', 'canal': item['canal']})
        li = xbmcgui.ListItem(item['title'], iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
    
    
def menu_mesdestacats():
    shows = tv3.get_mesdestacats()
    build_episodes_menu(shows, True)


def menu_mesvotats():
    shows = tv3.get_mesvotats()
    build_episodes_menu(shows, True)


def menu_mesvistos():
    shows = tv3.get_mesvistos()
    build_episodes_menu(shows, True)
    

def menu_programes():
    for letter in tv3.letters:
        url = build_url({'mode': 'letter', 'letter': letter})
        li = xbmcgui.ListItem(letter, iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True) 
    xbmcplugin.endOfDirectory(addon_handle)


def menu_letter(letter):
    shows = tv3.get_letter(letter)
    for show in shows:
        url = build_url({'mode': 'episodes', 'code': show.code})
        iconImage = show.img if len(show.img) > 0 else 'DefaultVideo.png'
        li = xbmcgui.ListItem(show.title, iconImage=iconImage)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True) 
    xbmcplugin.endOfDirectory(addon_handle)  
    
    
def menu_episodes(code):
    episodes = tv3.get_episodes(code)
    build_episodes_menu(episodes)
    
    
def menu_arafem(canal):
    rtmp = tv3.get_canal_stream(canal)
    xbmc.Player().play(rtmp)
    

def play(code):
    videos = tv3.get_media(code)
    video = videos[0]
    rtmp = tv3.get_show_rtmp(code, video.quality_code, video.format)
    xbmc.Player().play(rtmp)
    

def menu(mode):
    if mode is None:
        menu_mainmenu()
    elif mode == 'directe':
        menu_directe()
    elif mode == 'arafem':
        canal = args['canal'][0]
        menu_arafem(canal)
    elif mode == 'mesdestacats':
        menu_mesdestacats()
    elif mode == 'mesvistes':
        menu_mesvistos()
    elif mode == 'mesvotats':
        menu_mesvotats()
    elif mode == 'programes':
        menu_programes()
    elif mode == 'letter':
        letter = args['letter'][0]
        menu_letter(letter)
    elif mode == 'episodes':
        code = args['code'][0]
        menu_episodes(code)
    elif mode == 'play':
        code = args['code'][0]
        play(code)


mode = args.get('mode', None)
menu(mode[0] if mode else None)
