# -*- condig: utf-8 -*-
from sitic.content.base_content import BaseContent


class Section(BaseContent):
    paginable = True
    default_template_name = 'section'

    def __init__(self, name):
        self.name = name
        self.pages = []

    def add_page(self, page):
        if page not in self.pages:
            self.pages.append(page)
            page.section = self

    def get_url(self):
        url = '/'.join([self.name])
        return url

    def get_simple_context(self):
        context = {
            'name': self.name,
            'page_count': len(self.pages),
            'url': self.get_url(),
        }
        return context

    def get_context(self):
        context = self.get_simple_context()
        context['pages'] = [p.get_simple_context() for p in self.pages]
        return context

    def get_templates(self):
        return ["{}.html".format('section')]
