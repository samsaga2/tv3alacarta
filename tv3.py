import webutil
import xml.etree.ElementTree as ET
import urlparse
import urllib
import re


letters = ['#','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
page_url = 'http://zonatv.net/cadenas-autonomicas/tv-3-cat.php'
swf_url = 'http://zonatv.net/cadenas-autonomicas/media/canales/tv-3-cat-2654656.swf'


class Show:
    def __init__(self, title, code, img):
        self.title = title
        self.code = code
        self.img = img
        
        
class Episode:
    def __init__(self, title, subtitle, code, img, plot, date):
        self.title = title
        self.subtitle = subtitle
        self.code = code
        self.img = img
        self.plot = plot
        self.date = date


class Media:
    def __init__(self, format, quality_label, quality_code):
        self.format = format
        self.quality_label = quality_label
        self.quality_code = quality_code
                

def fetch_xml(url):
    xmlsrc = webutil.fetch_page(url)
    xmldoc = ET.fromstring(xmlsrc)
    return xmldoc


def build_show_item(item):
    title = item.find('titol').text.encode('ISO-8859-1')
    code = item.find('idint_rss').text
    try:
        img = item.find('imatges').findall('img')[0].text
    except:
        img = ''
    return Show(title, code, img)


def build_episode_item(item):
    code = item.attrib['idint']
    title = item.find('titol').text.encode('ISO-8859-1')
    subtitle = item.find('subtitol').text.encode('ISO-8859-1')
    try:
        img = item.find('imatges').findall('img')[0].text
    except:
        img = ''
    
    entradeta = item.find('entradeta').text
    if entradeta == None:
        entradeta = ''
    else:
        entradeta = entradeta.encode('ISO-8859-1')
    data = item.find('data').text 
    durada = item.find('durada_h').text
    plot = 'Data: {0}\nDurada: {1}\n{2}'.format(data, durada, entradeta)
    return Episode(title, subtitle, code, img, plot, data)
    

def build_media_item(video):
    format = video.find('format').text
    quality_label = video.find('qualitat').attrib['label']
    quality_code = video.find('qualitat').text
    return Media(format, quality_label, quality_code)
    
    
def get_mesdestacats():
    url = 'http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=destacats&page=1&pageItems=100&device=web'
    xmldoc = fetch_xml(url)    
    list = map(build_episode_item, xmldoc.find('resultats'))
    return list


def get_mesvotats():
    url = 'http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=mesvotats&page=1&pageItems=100&device=web'
    xmldoc = fetch_xml(url)
    list = map(build_episode_item, xmldoc.find('resultats'))
    return list


def get_mesvistos():
    url = 'http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=mesvistos&page=1&pageItems=10&device=web'
    xmldoc = fetch_xml(url)
    list = map(build_episode_item, xmldoc.find('resultats'))
    return list
         

def get_letter(letter):
    url = 'http://www.tv3.cat/p3ac/llistatProgramesLletra.jsp?lletra={0}&page=1&pageItems=1000'.format(letter)
    xmldoc = fetch_xml(url)
    list = map(build_show_item, xmldoc.find('resultats'))
    return list


def get_episodes(code):
    url = 'http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=videosprog&id={0}&page=1&pageItems=1000&device=web'.format(code)
    xmldoc = fetch_xml(url)
    list = map(build_episode_item, xmldoc.find('resultats')) 
    return list


def get_media(code):
    url = 'http://www.tv3.cat/pvideo/FLV_bbd_dadesItem.jsp?idint={0}'.format(code)
    xmldoc = fetch_xml(url)
    title = xmldoc.find('title').text
    videos = map(build_media_item, xmldoc.find('videos').findall('video'))
    return videos


def format_rmtp_url(rtmpurl):
    matches = re.findall("rtmp\://(.*?)/(.*?)/(.*?)$", rtmpurl, flags=re.DOTALL)
    rtmp_host = matches[0][0]
    rtmp_app = matches[0][1]
    rtmp_playpath = matches[0][2]
    return 'rtmp://{0} playpath={1} app={2} swfUrl={3} live=1 pageUrl={4}'.format(rtmp_host, rtmp_playpath, rtmp_app, swf_url, page_url)


def format_rmtpdirecte_url(rtmpurl):
    matches = re.findall("rtmp\://(.*?)/(.*?)/(.*?)$", rtmpurl, flags=re.DOTALL)
    rtmp_host = matches[0][0]
    rtmp_app = matches[0][1]
    rtmp_playpath = matches[0][2]
    return 'rtmp://{0}/{1} playpath={1} app={2} swfUrl={3} live=1 pageUrl={4}'.format(rtmp_host, rtmp_playpath, rtmp_app, swf_url, page_url)


def get_show_rtmp(code, quality_code, format):
    url = 'http://www.tv3.cat/pvideo/FLV_bbd_media.jsp?PROFILE=EVP&ID={0}&QUALITY={1}&FORMAT={2}'.format(code, quality_code, format)
    xmldoc = fetch_xml(url)
    media = xmldoc.find('item').find('media').text
    return format_rmtp_url(media)


def get_canal_stream(canal):
    url = 'http://www.tv3.cat/3ac/xml_dinamic/arafem/canal_{0}.xml'.format(canal)
    xmldoc = fetch_xml(url)
    default_quality = xmldoc.find('qualitat_defecte').text
    for stream in xmldoc.find('streams'):        
        qualitat = stream.attrib['qualitat']
        if qualitat == default_quality:
            for geo in stream.findall('geo'):
                if geo.attrib['ambit'] == 'TOTS':
                    url = geo.attrib['url']
                    xmldoc = tv3xml.fetch_xml(url)
                    media = xmldoc.find('item').find('media').text
                    return format_rmtpdirecte_url(media)
    return ''
