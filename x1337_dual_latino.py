# VERSION: 1.0r
# AUTHOR: mhoycss
# LICENSE: MIT
# qBittorrent Search Plugin for 1337x (prioritizing dual audio Latino)

import re
from novaprinter import prettyPrinter
from helpers import download_search_page

class x1337_dual_latino(object):
    url = 'https://www.1377x.to'
    name = 'x1337_dual_latino'
    supported_categories = {'all': ''}

    def search(self, what, cat='all'):
        results = []
        query = what.replace(' ', '%20')
        for page in range(1, 2):
            html = download_search_page(f'{self.url}/search/{query}/{page}/')
            if not html:
                continue

            rows = re.findall(
                r'<tr>.*?<a href="(/torrent/\d+/[^"]+)">([^<]+)</a>.*?'
                r'<td class="coll-4[^>]*>([^<]+)</td>.*?'
                r'<td class="coll-2[^>]*>(\d+)</td>.*?'
                r'<td class="coll-3[^>]*>(\d+)</td>',
                html,
                re.DOTALL
            )

            for link, title, size, seeds, leech in rows:
                torrent = {
                    'name': title,
                    'size': size.strip(),
                    'seeds': int(seeds),
                    'leech': int(leech),
                    'engine_url': self.url,
                    'desc_link': self.url + link,
                    'link': self.url + link
                }
                results.append(torrent)

        # Reorganiza: primero los que contienen palabras clave
        filtered = [r for r in results if re.search(r'dual|latino|castellano|esp', r['name'], re.I)]
        others = [r for r in results if r not in filtered]
        for torrent in filtered + others:
            prettyPrinter(torrent)
