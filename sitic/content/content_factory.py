# -*- condig: utf-8 -*-
import os

from sitic.config import config
from sitic.content import Page, page_parser
from sitic.content.taxonomy import TaxonomyDefinition, Taxonomy


class ContentFactory(object):
    contents = []
    taxonomy_definitions = {}
    taxonomies = {}

    def get_contents(self, contents_path):
        self.taxonomy_definitions = {
            singular: TaxonomyDefinition(singular, plural)
            for singular, plural in config.get_taxonomies().items()
        }
        for path in contents_path:
            content = self.get_content(path)
            self.contents.append(content)
            self.update_taxonomies(content)

        return self.contents

    def get_content(self, content_path):
        frontmatter, content = page_parser.load(content_path)

        relative_path = content_path.replace(config.content_path, "").strip(os.sep)
        path_chunks = relative_path.split(os.sep)
        name = path_chunks[-1]
        section = None
        if len(path_chunks) > 1:
            section = path_chunks[0]

        return Page(frontmatter, content, name, path_chunks, section)

    def update_taxonomies(self, content):
        for singular, plural in config.get_taxonomies().items():
            terms = content.frontmatter.get(plural, [])
            definition = self.taxonomy_definitions[singular]
            for term in terms:
                term = term.lower()
                if term not in self.taxonomies:
                    self.taxonomies[term] = Taxonomy(term, definition)
                self.taxonomies[term].add_page(content)

    def get_taxonomies(self):
        return list(self.taxonomies.values())
