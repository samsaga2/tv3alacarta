import urllib2
import re

def fetch_page(url):
    headers = {
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'
    }
    request = urllib2.Request(url, headers=headers)
    return urllib2.urlopen(request).read()


def format_rmtp_url(rtmpurl):
    # from 'rtmp://mp4-500-strfs.fplive.net/mp4-500-str/mp4:g/tvcatalunya/0/0/1381401675900.mp4'
    # to 'rtmp://mp4-500-strfs.fplive.net playpath=mp4:g/tvcatalunya/0/0/1381401675900.mp4 app=mp4-500-str'
    matches = re.findall("rtmp\://(.*?)/(.*?)/(.*?)$", rtmpurl, flags=re.DOTALL)
    rtmp_host = matches[0][0]
    rtmp_app = matches[0][1]
    rtmp_playpath = matches[0][2]
    return 'rtmp://{0} playpath={1} app={2}'.format(rtmp_host, rtmp_playpath, rtmp_app)
