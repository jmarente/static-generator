# -*- condig: utf-8 -*-
from sitic.content.base_content import BaseContent


class Homepage(BaseContent):
    paginable = True
    content_page = None

    def __init__(self):
        self.name = 'Homepage'
        self.pages = []

    def set_content_page(self, page):
        self.content_page = page

    def get_url(self):
        return '/'

    def get_simple_context(self):
        if self.simple_context is None:
            self.simple_context = {
                'name': self.name,
                'page_count': len(self.pages),
                'url': self.get_url(),
            }
            if self.content_page:
                self.simple_context['page'] = self.content_page.get_simple_context()
        return self.simple_context

    def get_context(self):
        if self.context is None:
            self.context = self.get_simple_context()
            self.context['pages'] = [p.get_simple_context() for p in self.pages]
            if self.content_page:
                self.context['page'] = self.content_page.get_context()
        return self.context

    def get_templates(self):
        return [
            "index.html",
            "default/list.html",
            "default/page.html",
        ]
