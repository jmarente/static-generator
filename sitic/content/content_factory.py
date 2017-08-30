# -*- condig: utf-8 -*-
import os
import json
from collections import defaultdict

from sitic.config import config
from sitic.content import Page, page_parser
from sitic.content.taxonomy import TaxonomyDefinition, Taxonomy
from sitic.content.section import Section
from sitic.content.homepage import Homepage
from sitic.content.routed_page import RoutedPage
from sitic.content.rss import Rss
from sitic.content.search_page import SearchPage
from sitic.utils import constants
from sitic.logging import logger


class ContentFactory(object):
    contents = defaultdict(list)
    expired_contents = defaultdict(list)

    taxonomy_definitions = {}
    taxonomies = defaultdict(dict)
    sections = defaultdict(dict)
    rss = defaultdict(list)

    homepages = {}

    def initialize(self):
        self.contents = defaultdict(list)
        self.expired_contents = defaultdict(list)

        self.taxonomy_definitions = {}
        self.taxonomies = defaultdict(dict)
        self.sections = defaultdict(dict)
        self.rss = defaultdict(list)
        self.search_pages = {}

        self.homepages = {}
        for lang in config.get_languages():
            self.homepages[lang] = homepage = Homepage(lang)
            self.rss[lang].append(Rss(lang, homepage))
            self.search_pages[lang] = SearchPage(lang)

    def build_contents(self):
        self.initialize()
        for root, directory, files in os.walk(config.content_path):
            supported_files = [os.path.join(root, f) for f in files
                    if f.endswith(tuple(constants.VALID_CONTENT_EXTENSIONS))]
            self._build_contents(supported_files)

        self.build_routed_contents()

    def _build_contents(self, contents_path):
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
        extension = filename_parts[-1]
        if len(filename_parts) > 2:
            posible_lang = filename_parts[-2]
            language = posible_lang if posible_lang in languages else language
            name = "_".join(filename_parts[0:-2])


        page_path = path_chunks[0:-1]
        section = None
        page = Page(frontmatter, content, name, extension, relative_path, page_path, language)
        page.set_modification_date(os.path.getmtime(content_path))
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

            if plural not in self.taxonomies[content.language]:
                self.taxonomies[content.language][plural] = {}

            for term in terms:
                term = term.lower()
                if term not in self.taxonomies[content.language][plural]:
                    self.taxonomies[language][plural][term] = taxonomy = Taxonomy(term, definition, language)
                    self.rss[language].append(Rss(language, taxonomy))
                self.taxonomies[language][plural][term].add_page(content)

    def get_taxonomies(self, language):
        return self.taxonomies[language]

    def get_sections(self, language):
        return list(self.sections[language].values())

    def get_contents(self, language):
        return self.contents[language]

    def _get_section(self, section_name, language):
        section = self.sections[language].get(section_name, None)
        if section is None:
            self.sections[language][section_name] = section = Section(section_name, language)
            self.rss[language].append(Rss(language, section))

        return section

    def build_routed_contents(self):
        routing_content = self.get_routing_content()

        for content in routing_content:
            try:
                routed_page = self.handle_routed_content(content)
            except Exception as e:
                logger.warning('Routed config with data {} could not be handle. Error: {}'
                               .format(json.dumps(content), str(e)))

            language = routed_page.language
            if routed_page.to_publish():
                self.contents[language].append(routed_page)
            elif routed_page.is_expired():
                self.expired_contents[language].append(routed_page)

    def handle_routed_content(self, content):

        languages = config.get_languages()

        if not isinstance(content, dict):
            logger.warning('Every element in the routing file must be a dictionary: {}'.format(e.message))
            return

        language = config.main_language
        if 'language' in content:
            language = content['language'] if content['language'] in languages else language
            del content['language']

        section_name = None
        if 'section' in content:
            section_name = content.get('section')
            del content['section']

        routed_page = RoutedPage(content, language)

        if routed_page.to_publish():
            section = self._get_section(section_name, language)
            section.add_page(routed_page)

            self.update_taxonomies(routed_page)

        return routed_page

    def get_routing_content(self):
        content = []
        if os.path.isfile(config.routing_path):
            with open(config.routing_path) as routing_file:
                try:
                    content = json.load(routing_file)
                except Exception as e:
                    logger.warning('Routing file could not be parsed: {}'.format(e.message))

        if not isinstance(content, list):
            logger.warning('Routing file wrong format: {}'.format(e.message))
            content = []
        return content
