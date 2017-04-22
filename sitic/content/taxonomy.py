# -*- condig: utf-8 -*-
from sitic.content.base_content import BaseContent


class TaxonomyDefinition(object):
    singular = ''
    plural = ''

    def __init__(self, singular, plural):
        self.singular = singular
        self.plural = plural


class Taxonomy(BaseContent):
    paginable = True

    def __init__(self, name, definition=None):
        self.name = name
        self.definition = definition
        self.pages = []

    def add_page(self, page):
        if page not in self.pages:
            self.pages.append(page)
            page.add_taxonomy(self)

    def get_url(self):
        url = '/'.join([self.definition.singular, self.name])
        return url

    def get_simple_context(self):
        if self.simple_context is None:
            self.simple_context = {
                'taxonomy': self.definition.singular,
                'name': self.name,
                'page_count': len(self.pages),
                'url': self.get_url(),
            }
        return self.simple_context

    def get_context(self):
        if self.context is None:
            self.context = self.get_simple_context()
            self.context['pages'] = [p.get_simple_context() for p in self.pages]
        return self.context

    def get_templates(self):
        return [
            "taxonomy/{}.html".format(self.definition.singular),
            "taxonomy/list.html",
            "default/taxonomy.html",
            "default/list.html"
        ]
