import webutil
import xml.etree.ElementTree as ET
import re
import urlparse
import urllib


letters = ['#','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


def fetch_xml(url):
    xmlsrc = webutil.fetch_page(url)
    xmldoc = ET.fromstring(xmlsrc)
    return xmldoc


def fetch_mesdestacats():
    # http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=destacats&id=&page=1&pageItems=10&device=web
    url = 'http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=destacats&page=1&pageItems=100&device=web'
    return fetch_xml(url)


def fetch_mesvotats():
    # http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=mesvotats&page=1&pageItems=10&device=web
    url = 'http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=mesvotats&page=1&pageItems=100&device=web'
    return fetch_xml(url)


def fetch_mesvistos():
    # http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=mesvistos&page=1&pageItems=10&device=web
    url = 'http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=mesvistos&page=1&pageItems=10&device=web'
    return fetch_xml(url)


def fetch_xmlletter(letter):
    # http://www.tv3.cat/p3ac/llistatProgramesLletra.jsp?lletra=A&page=1&pageItems=1000
    url = 'http://www.tv3.cat/p3ac/llistatProgramesLletra.jsp?lletra={0}&page=1&pageItems=1000'.format(letter)
    return fetch_xml(url)


def fetch_xmlinfo(code):
    url = 'http://www.tv3.cat/pvideo/FLV_bbd_dadesItem.jsp?idint={0}'.format(code)
    return fetch_xml(url)


def fetch_xmlepisodes(code):
    # http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=videosprog&id=50338&page=1&pageItems=1000&device=web
    url = 'http://www.tv3.cat/p3ac/p3acLlistatVideos.jsp?type=videosprog&id={0}&page=1&pageItems=1000&device=web'.format(code)
    return fetch_xml(url)


def fetch_xmlmedia(code, quality, format):
    url = 'http://www.tv3.cat/pvideo/FLV_bbd_media.jsp?PROFILE=EVP&ID={0}&QUALITY={1}&FORMAT={2}'.format(code, quality, format)
    return fetch_xml(url)


def fetch_xml_canal(canal):
    # http://www.tv3.cat/3ac/xml_dinamic/arafem/canal_TV3CAT.xml
    url = 'http://www.tv3.cat/3ac/xml_dinamic/arafem/canal_{0}.xml'.format(canal)
    return fetch_xml(url)
