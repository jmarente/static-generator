# -*- condig: utf-8 -*-
import os
from collections import defaultdict

from sitic.config import config
from sitic.content import Page, page_parser
from sitic.content.taxonomy import TaxonomyDefinition, Taxonomy
from sitic.content.section import Section
from sitic.content.homepage import Homepage
from sitic.utils import constants


class ContentFactory(object):
    contents = defaultdict(list)
    expired_contents = defaultdict(list)

    taxonomy_definitions = {}
    taxonomies = defaultdict(dict)
    sections = defaultdict(dict)

    homepages = {}

    def __init__(self):
        for lang in config.get_languages():
            self.homepages[lang] = Homepage(lang)

    def build_contents(self, contents_path):
        self.taxonomy_definitions = {
            singular: TaxonomyDefinition(singular, plural)
            for singular, plural in config.get_taxonomies().items()
        }
        for path in contents_path:
            content = self._get_content(path)
            if content:
                if content.to_publish():
                    self.contents[content.language].append(content)
                elif content.is_expired():
                    self.expired_contents[content.language].append(content)

        return self.contents

    def _get_content(self, content_path):
        frontmatter, content = page_parser.load(content_path)

        relative_path = content_path.replace(config.content_path, "").strip(os.sep)
        path_chunks = relative_path.split(os.sep)
        filename = path_chunks[-1]

        language = config.main_language
        languages = config.get_languages()
        filename_parts = filename.split('.')
        name = "_".join(filename_parts[0:-1])
        if len(filename_parts) > 2:
            posible_lang = filename_parts[-2]
            language = posible_lang if posible_language in languages else language
            name = "_".join(filename_parts[0:-2])


        page_path = path_chunks[0:-1]
        section = None
        page = Page(frontmatter, content, name, page_path, language)
        page_is_section = False
        page_is_homepage = False

        if len(path_chunks) > 1:
            section_name = path_chunks[0]
        elif page.name == 'index':
            page_is_homepage = True
        else:
            page_is_section = True
            section_name = page.name

        # Index content means section content
        if len(path_chunks) == 2 and page.name == 'index':
            page_is_section = True

        page_to_return = page
        if page_is_homepage:
            page_to_return = None
            self.homepages[language].set_content_page(page)
        elif page.to_publish():
            section = self._get_section(section_name, language)
            if page_is_section:
                section.set_content_page(page)
                page_to_return = None
            else:
                section.add_page(page)

            self.update_taxonomies(page)

        return page_to_return


    def update_taxonomies(self, content):
        language = content.language
        for singular, plural in config.get_taxonomies().items():
            terms = content.frontmatter.get(plural, [])
            definition = self.taxonomy_definitions[singular]
            for term in terms:
                term = term.lower()
                if term not in self.taxonomies[content.language]:
                    self.taxonomies[language][term] = Taxonomy(term, definition, language)
                self.taxonomies[language][term].add_page(content)

    def get_taxonomies(self, language):
        return list(self.taxonomies[language].values())

    def get_sections(self, language):
        return list(self.sections[language].values())

    def get_contents(self, language):
        return self.contents[language]

    def _get_section(self, section_name, language):
        section = self.sections[language].get(section_name, None)
        if section is None:
            self.sections[language][section_name] = section = Section(section_name, language)

        return section
