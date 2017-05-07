# -*- condig: utf-8 -*-
from sitic.content.base_content import BaseContent
from sitic.config import config

class Sitemap(BaseContent):
    url_file = 'sitemap.xml'

    def __init__(self, language):
        super(Sitemap, self).__init__()
        self.name = 'Sitemap'
        self.language = language
        self.contents = []
        self._priority = self._change_frequency = None
        if config.sitemap and isinstance(config.sitemap, dict):
            self._priority = config.sitemap.get('priority', None)
            self._change_frequency = config.sitemap.get('change_frequency', None)

    def _get_url(self):
       return '/'

    def get_templates(self):
        return [
            "sitemap.xml",
        ]

    def get_context(self):
        context = super(Sitemap, self).get_context()
        context['pages'] = [c.get_simple_context() for c in self.contents]
        context['priority'] = self.priority
        context['change_frequency'] = self.change_frequency
        return context

    def priority(self, page=None):
        page_config = page.get('sitemap', None)
        if page_config and isinstance(page_config, dict) and page_config.get('priority', None):
            return page_config.get('priority')
        return self._priority

    def change_frequency(self, page=None):
        page_config = page.get('sitemap', None)
        if page_config and isinstance(page_config, dict) and page_config.get('change_frequency', None):
            return page_config.get('change_frequency')
        return self._change_frequency
