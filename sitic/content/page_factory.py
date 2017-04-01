# -*- condig: utf-8 -*-
import os

from sitic.config import config
from sitic.content import Page, page_parser
from sitic.content.taxonomy import TaxonomyDefinition, Taxonomy


class PageFactory(object):
    pages = []
    taxonomy_definitions = {}
    taxonomies = {}

    def get_pages(self, pages_path):
        self.taxonomy_definitions = {
            singular: TaxonomyDefinition(singular, plural)
            for singular, plural in config.get_taxonomies().items()
        }
        for path in pages_path:
            page = self.get_page(path)
            self.pages.append(page)
            self.update_taxonomies(page)

        return self.pages

    def get_page(self, page_path):
        frontmatter, content = page_parser.load(page_path)

        relative_path = page_path.replace(config.content_path, "").strip(os.sep)
        path_chunks = relative_path.split(os.sep)
        name = path_chunks[-1]
        sections = []
        if len(path_chunks) > 1:
            sections = path_chunks[:-1]

        return Page(frontmatter, content, name, sections)

    def update_taxonomies(self, page):
        for singular, plural in config.get_taxonomies().items():
            terms = page.frontmatter.get(plural, [])
            definition = self.taxonomy_definitions[singular]
            for term in terms:
                term = term.lower()
                if term not in self.taxonomies:
                    self.taxonomies[term] = Taxonomy(term, definition)
                self.taxonomies[term].add_page(page)
