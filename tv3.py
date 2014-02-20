import webutil
import re
import tv3xml


letters = ['#','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


class Show:
    def __init__(self, title, code, img):
        self.title = title
        self.code = code
        self.img = img
        
        
class Episode:
    def __init__(self, title, code, img, plot, date):
        self.title = title
        self.code = code
        self.img = img
        self.plot = plot
        self.date = date


class Media:
    def __init__(self, format, quality_label, quality_code):
        self.format = format
        self.quality_label = quality_label
        self.quality_code = quality_code
         

def get_letter(letter):
    def build_item(item):
        titol = item.find('titol').text
        code = item.find('idint_rss').text
        try:
            img = item.find('imatges').findall('img')[0].text
        except:
            img = ''
        return Show(titol, code, img)
    xmldoc = tv3xml.fetch_xmlletter(letter)
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
        return Episode(titol, code, img, plot, data)
    xmldoc = tv3xml.fetch_xmlepisodes(code)
    list = map(build_item, xmldoc.find('resultats')) 
    return list


def get_media(code):
    def extract_video_info(video):
        format = video.find('format').text
        quality_label = video.find('qualitat').attrib['label']
        quality_code = video.find('qualitat').text
        return Media(format, quality_label, quality_code)
    xmldoc = tv3xml.fetch_xmlinfo(code)
    title = xmldoc.find('title').text
    videos = map(extract_video_info, xmldoc.find('videos').findall('video'))
    return videos


def get_show_rtmp(code, quality_code, format):
    xmldoc = tv3xml.fetch_xmlmedia(code, quality_code, format)
    media = xmldoc.find('item').find('media').text
    return webutil.format_rmtp_url(media)
