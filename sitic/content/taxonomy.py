# -*- condig: utf-8 -*-
from sitic.content.paginable_content import PaginableContent


class TaxonomyDefinition(object):
    singular = ''
    plural = ''

    def __init__(self, singular, plural):
        self.singular = singular
        self.plural = plural


class Taxonomy(PaginableContent):

    def __init__(self, name, definition=None, language=None):
        super(Taxonomy, self).__init__()
        self.name = name
        self.definition = definition
        self.language = language

    def add_page(self, page):
        super(Taxonomy, self).add_page(page)
        page.add_taxonomy(self)

    def get_url(self):
        url = '/'.join([self.definition.singular, self.name])
        return url

    def get_simple_context(self):
        if self.simple_context is None:
            super(Taxonomy, self).get_simple_context()
            self.simple_context['taxonomy'] = self.definition.singular
        return self.simple_context

    def get_templates(self):
        return [
            "taxonomy/{}.html".format(self.definition.singular),
            "taxonomy/list.html",
            "default/taxonomy.html",
            "default/list.html"
        ]
