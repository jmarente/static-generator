# -*- condig: utf-8 -*-
from sitic.content.base_content import BaseContent

class Sitemap(BaseContent):
    url_file = 'sitemap.xml'

    def __init__(self, language):
        super(Sitemap, self).__init__()
        self.name = 'Sitemap'
        self.language = language
        self.contents = []

    def _get_url(self):
       return '/'

    def get_templates(self):
        return [
            "sitemap.xml",
        ]

    def get_context(self):
        context = super(Sitemap, self).get_context()
        context['pages'] = [c.get_simple_context() for c in self.contents]
        return context
