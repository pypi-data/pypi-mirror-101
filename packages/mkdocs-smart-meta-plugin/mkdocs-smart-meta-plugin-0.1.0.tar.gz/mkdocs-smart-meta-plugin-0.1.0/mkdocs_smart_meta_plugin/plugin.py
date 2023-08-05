from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Page
from mkdocs.config import config_options

from bs4 import BeautifulSoup, NavigableString, CData

import urllib.parse


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


class SmartMetaPlugin(BasePlugin):
    config_scheme = (
    )

    def on_page_content(
            self, html: str, page: Page, config: config_options.Config, files, **kwargs
    ) -> str:
        soup = BeautifulSoup(html, 'html.parser')

        description = ''

        for descendant in soup.descendants:
            if type(descendant) not in (NavigableString, CData):
                continue
            if descendant.parent.name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                continue
            descendant = descendant.strip()
            if len(descendant) == 0:
                continue
            if descendant == '¶':
                continue
            description += descendant + ' '

        page.meta['smart_description'] = ' '.join(description.strip().split()[:25]) + '...'

        image = soup.img
        if image is not None:
            path = remove_prefix(image['src'], '../')
            page.meta['smart_image'] = urllib.parse.urljoin(config['site_url'], path)

        return html
