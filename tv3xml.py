import webutil
import xml.etree.ElementTree as ET
import re
import urlparse
import urllib


letters = ['#','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def _fetch_xml(url):
    xmlsrc = webutil.fetch_page(url)
    xmldoc = ET.fromstring(xmlsrc)
    return xmldoc


def fetch_xmlletter(letter):
    # http://www.tv3.cat/p3ac/llistatProgramesLletra.jsp?lletra=A&page=1&pageItems=1000
    url = 'http://www.tv3.cat/p3ac/llistatProgramesLletra.jsp?lletra={0}&page=1&pageItems=1000'.format(letter)
    return _fetch_xml(url)


def fetch_xmlinfo(code):
    url = 'http://www.tv3.cat/pvideo/FLV_bbd_dadesItem.jsp?idint={0}'.format(code)
    return _fetch_xml(url)


def fetch_xmlepisodes(code):
    # http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=videosprog&id=50338&page=1&pageItems=1000&device=web
    url = 'http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=videosprog&id={0}&page=1&pageItems=1000&device=web'.format(code)
    return _fetch_xml(url)


def fetch_xmlmedia(code, quality, format):
    url = 'http://www.tv3.cat/pvideo/FLV_bbd_media.jsp?PROFILE=EVP&ID={0}&QUALITY={1}&FORMAT={2}'.format(code, quality, format)
    return _fetch_xml(url)


def get_letter(letter):
    def build_item(item):
        titol = item.find('titol').text
        code = item.find('idint_rss').text
        try:
            img = item.find('imatges').findall('img')[0].text
        except:
            img = ''
        return {'titol': titol, 'code': code, 'img': img}
    xmldoc = fetch_xmlletter(letter)
    list = map(build_item, xmldoc.find('resultats'))
    return list


def get_episodes(code):
    def build_item(item):
        code = item.attrib['idint']
        titol = item.find('titol').text
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
        return {'code': code,
                'titol': titol,
                'img': img,
                'plot': plot,
                'data': data                    
                }
    xmldoc = fetch_xmlepisodes(code)
    list = map(build_item, xmldoc.find('resultats')) 
    return list


def get_show_info(code):
    def extract_video_info(video):
        format = video.find('format').text
        quality_label = video.find('qualitat').attrib['label']
        quality_code = video.find('qualitat').text
        return {'format':format, 'quality_label':quality_label, 'quality_code':quality_code}    
    xmldoc = fetch_xmlinfo(code)
    title = xmldoc.find('title').text
    videos = map(extract_video_info, xmldoc.find('videos').findall('video'))
    return {'title':title, 'videos':videos}


def get_show_rtmp(code, quality_code, format):
    xmldoc = fetch_xmlmedia(code, quality_code, format)
    media = xmldoc.find('item').find('media').text
    return webutil.format_rmtp_url(media)

