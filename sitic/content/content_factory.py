# -*- condig: utf-8 -*-
import os

from sitic.config import config
from sitic.content import Page, page_parser
from sitic.content.taxonomy import TaxonomyDefinition, Taxonomy
from sitic.content.section import Section


class ContentFactory(object):
    contents = []
    taxonomy_definitions = {}
    taxonomies = {}
    sections = {}

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
        filename = path_chunks[-1]
        content_path = path_chunks[0:-1]
        section = None
        page = Page(frontmatter, content, filename, content_path)
        if len(path_chunks) > 1:
            section_name = path_chunks[0]
        else:
            section_name = page.name

        section = self._get_section(section_name)
        section.add_page(page)

        return page


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

    def get_sections(self):
        return list(self.sections.values())

    def _get_section(self, section_name):
        section = self.sections.get(section_name, None)
        if section is None:
            self.sections[section_name] = section = Section(section_name)

        return section
