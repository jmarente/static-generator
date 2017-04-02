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
    default_template_name = None

    def __init__(self, name, definition=None):
        self.name = name
        self.definition = definition
        self.pages = []

    def add_page(self, page):
        self.pages.append(page)
        page.taxonomies.append(self)

    def get_url(self):
        url = '/'.join([self.definition.singular, self.name])
        return url

    def get_simple_context(self):
        context = {
            'taxonomy': self.definition.singular,
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
        templates = super(Taxonomy, self).get_templates()

        templates.append('{}.html'.format(self.definition.singular))
        templates.append('{}.html'.format(self.definition.plural))
        templates.append("{}.html".format('taxonomy'))

        return templates
