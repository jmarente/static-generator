# -*- condig: utf-8 -*-
from sitic.content.base_content import BaseContent
from sitic.config import config

class Rss(BaseContent):
    url_file = 'index.xml'

    def __init__(self, language, content):
        super(Rss, self).__init__()
        self.name = 'Rss'
        self.language = language
        self.content = content

        content.set_rss(self)

    def _get_url(self):
       return self.content._get_url()

    def get_templates(self):
        return [
            "rss.xml",
        ]

    def get_context(self):
        context = super(Rss, self).get_context()
        context['content'] = self.content.get_simple_context()
        context['pages'] = [p.get_context() for p in self.content.get_pages()[:config.rss_limit]]
        return context
