# -*- condig: utf-8 -*-
from sitic.content.base_content import BaseContent


class TaxonomyDefinition(object):
    singular = ''
    plural = ''

    def __init__(self, singular, plural):
        self.singular = singular,
        self.plural = plural


class Taxonomy(BaseContent):

    def __init__(self, name, definition=None):
        self.name = name
        self.definition = definition
        self.pages = []

    def add_page(self, page):
        self.pages.append(page)
        page.taxonomies.append(self)

    def get_url(self):
        raise NotImplementedError()

    def get_context(self):
        raise NotImplementedError()

    def get_path(self):
        raise NotImplementedError()
