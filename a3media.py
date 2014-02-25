import webutil


def build_mainmenu(section):
    title = section.find('title').text
    img = section.find('urlImage').text
    id = section.find('idSection').text
    return {'title': title.encode('utf-8'),
            'img': img.replace('.jpg', '01.jpg').encode('utf-8') if img else '',
            'id': id.encode('utf-8')}


def build_section(item):
    section = item.find('section')
    title = section.find('title').text
    img = section.find('urlImage').text
    id = section.find('idSection').text
    plot = section.find('seoDescription').text
    return {'title': title.encode('utf-8'),
            'img': img.replace('.jpg', '01.jpg').encode('utf-8') if img else '',
            'id': id.encode('utf-8'),
            'plot': plot.encode('utf-8')}
    
    
def build_episode(item):
    episode = item.find('episode')
    title = episode.find('title').text
    type = episode.find('type').text
    if type != 'FREE':
        title += '[{0}]'.format(type)
    img = episode.find('urlImage').text
    id = episode.find('contentPk').text
    plot = episode.find('storyline').text if episode.find('storyline') else ''
    return {'title': title.encode('utf-8'),
            'img': img.replace('.jpg', '01.jpg').encode('utf-8') if img else '',
            'id': id.encode('utf-8'),
            'plot': plot.encode('utf-8')}


def get_mainmenu():
    url = 'http://servicios.atresplayer.com/api/mainMenu'
    xmldoc = webutil.fetch_xml(url)
    sections = xmldoc.find('a').find('mainItem').find('menuItems').findall('section')
    return map(build_mainmenu, sections)


def get_section(id):
    url = 'http://servicios.atresplayer.com/api/categorySections/{0}'.format(id)
    xmldoc = webutil.fetch_xml(url)
    items = xmldoc.findall('item')
    return sorted(map(build_section, items), key=lambda x: x['title'])


def get_subcategories(id, subid):
    url = 'http://servicios.atresplayer.com/api/categorySections/{0}'.format(id)
    xmldoc = webutil.fetch_xml(url)
    for item in xmldoc.findall('item'):
        section = item.find('section')        
        if section.find('idSection').text == subid:
            subcategories = section.findall('subCategories')
            return map(build_section, subcategories)
    return []


def get_episodes(id):
    url = 'http://servicios.atresplayer.com/api/episodes/{0}'.format(id)
    xmldoc = webutil.fetch_xml(url)
    episodes = xmldoc.find('episodes').findall('item')
    # TODO extras
    return map(build_episode, episodes)
