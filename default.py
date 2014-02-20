# URL INFO http://www.tv3.cat/pvideo/FLV_bbd_dadesItem.jsp?idint=4705751
# URL RTMP http://www.tv3.cat/pvideo/FLV_bbd_media.jsp?PROFILE=EVP&ID=4705751&QUALITY=H&FORMAT=MP4
#    el QUALITY y el FORMAT salen del URL INFO



REMOTE_DBG = False 
if REMOTE_DBG:
    try:
        import pysrc.pydevd as pydevd
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)
        

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

mode = args.get('mode', None)


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


def build_letters_menu(letters):
    for letter in letters:
        url = build_url({'mode': 'letter', 'letter': letter})
        li = xbmcgui.ListItem(letter, iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True) 
    xbmcplugin.endOfDirectory(addon_handle)
    

def build_shows_menu(shows):
    for show in shows:
        url = build_url({'mode': 'episodes', 'code': show.code})
        li = xbmcgui.ListItem(show.title, iconImage=show.img)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True) 
    xbmcplugin.endOfDirectory(addon_handle)
    
    
def build_episodes_menu(episodes):
    for episode in episodes:
        url = build_url({'mode': 'play', 'code': episode.code})
        li = xbmcgui.ListItem(episode.title, iconImage="DefaultVideo.png", thumbnailImage=episode.img)
        li.setInfo("Video", {"Title": episode.title, "Plot": episode.plot, "Date": episode.date})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True) 
    xbmcplugin.endOfDirectory(addon_handle)


def show_mainmenu():
    url = build_url({'mode': 'programes'})
    li = xbmcgui.ListItem('Programes', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'mesdestacats'})
    li = xbmcgui.ListItem('Mes destacats', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'mesvistes'})
    li = xbmcgui.ListItem('Mes vistes', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'mesvotades'})
    li = xbmcgui.ListItem('Mes votades', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
     
    xbmcplugin.endOfDirectory(addon_handle)


def show_letters():
    build_letters_menu(tv3.letters)


def show_letter(letter):
    shows = tv3.get_letter(letter)
    build_shows_menu(shows)
    
    
def show_episodes(code):
    episodes = tv3.get_episodes(code)
    build_episodes_menu(episodes)
    
    
def play(code):
    videos = tv3.get_media(code)
    video = videos[0]
    url = tv3.get_show_rtmp(code, video.quality_code, video.format)
    xbmc.Player().play(url)
    

if mode is None:
    show_mainmenu()
elif mode[0] == 'mesdestacades':
    pass
elif mode[0] == 'mesvistes':
    pass
elif mode[0] == 'mesvotades':
    pass
elif mode[0] == 'programes':
    show_letters()
elif mode[0] == 'letter':
    letter = args['letter'][0]
    show_letter(letter)
elif mode[0] == 'episodes':
    code = args['code'][0]
    show_episodes(code)
elif mode[0] == 'play':
    code = args['code'][0]
    play(code)
