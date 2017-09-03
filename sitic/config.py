# -*- condig: utf-8 -*-
import os
import sys
import re
from collections import defaultdict

import yaml

from sitic.utils import constants
from sitic.logging import logger


class _Config():
    config = None
    verbose = False
    base_url = ""
    base_path = None
    content_path = None
    public_path = None
    static_path = None
    templates_path = None
    extra_params = {}
    ignore_files_regex = []
    build_draft = False
    build_future = False
    build_expired = False
    paginable = None # no pagination by default
    menus = {}
    lazy_menu = None
    languages = defaultdict(dict)
    main_language = None
    main_language_as_root= True
    sitemap = None
    rss_limit = constants.DEFAULT_RSS_LIMIT
    description_length = constants.DEFAULT_DESCRIPTION_LENGTH
    routing_path = None
    taxonomies = None
    taxonomies_by_lang = defaultdict(dict)
    disqus_shortname = ''
    search_enabled = True
    search_pagination = -1

    def load_config(self, config_file_path):
        self.config_path = config_file_path

        self.base_path = os.path.dirname(os.path.abspath(self.config_path))

        # Default
        self.content_path = os.path.join(self.base_path, constants.DEFAULT_CONTENT_PATH)
        self.public_path = os.path.join(self.base_path, constants.DEFAULT_PUBLIC_PATH)
        self.static_path = os.path.join(self.base_path, constants.DEFAULT_STATIC_PATH)
        self.templates_path = os.path.join(self.base_path, constants.DEFAULT_TEMPLATES_PATH)
        self.locales_path = os.path.join(self.base_path, constants.DEFAULT_LOCALES_PATH)
        self.routing_path = os.path.join(self.base_path, constants.DEFAULT_ROUTING_FILE_PATH)

        path_options = ['public_path', 'content_path', 'static_path']
        with open(self.config_path, 'r') as config_file:
            parsed_config = yaml.load(config_file)

            if not parsed_config:
                logger.warning('Config file completely empty')
                parsed_config = []

            for param in parsed_config:
                value = parsed_config[param]
                if param in path_options:
                    value = value if os.path.isdir(value) else os.path.join(self.base_path, value)
                setattr(self, param, value)

        if not os.path.isdir(self.content_path):
            logger.error('Invalid path for content. Folder not found')
            sys.exit(1)

        # TODO: make patterns configurables
        self.ignore_files_regex = [re.compile(i) for i in constants.IGNORE_FILES_PATTERN]

        self._format_languages()
        self.set_main_language()

        self.check_taxonomies_format()

        current_file_path = os.path.abspath(os.path.dirname(__file__))
        self.files_path = os.path.join(current_file_path, 'files/')

    def get_taxonomies(self, language):
        # TODO make it configurable
        taxonomies = self.taxonomies
        language_taxonomies = self.taxonomies_by_lang.get(language, None)
        if language_taxonomies:
            taxonomies = language_taxonomies
        return taxonomies

    def get_menus(self, language = None):
        menus = self.menus.copy()
        language_config = self.get_language_config(language)
        if language != constants.DEFAULT_LANG:
            language_menus = language_config.get('menus', {})
            if language == self.main_language:
                menus.update(language_menus)
            else:
                menus = language_menus
        return menus

    def _format_languages(self):
        pass

    def get_language_config(self, language):
        config = self.languages.get(language, {})
        if not config and not isinstance(config, dict):
            config = {}
        config['url'] = '/' + language if self.main_language != language or not self.main_language_as_root else '/'
        return config

    def get_languages_config(self):
        config = {}
        for language in self.get_languages():
            config[language] = self.get_language_config(language)
        return config

    def get_languages(self):
        languages = [constants.DEFAULT_LANG]
        if self.languages:
            languages = sorted(list(self.languages.keys()))
        return languages

    def set_main_language(self):
        main = self.main_language
        languages = self.get_languages()
        if self.languages and \
           (not self.main_language \
            or self.main_language not in languages):
            main = languages[0]
            logger.warning("main_language not correctly defined, "
                           "taking «{}» as main language".format(main))

        self.main_language = main

    def check_taxonomies_format(self):

        taxonomies_to_check = {}

        if self.taxonomies is not None:
            taxonomies_to_check['global'] = self.taxonomies

        # Any language defined
        if self.main_language is not None:
            for language in self.get_languages():
                config = self.get_language_config(language)
                taxonomies = config.get('taxonomies', None)
                if taxonomies is not None:
                    taxonomies_to_check[language] = taxonomies

        self.taxonomies = {}
        for config_key in taxonomies_to_check:
            taxonomies = taxonomies_to_check[config_key]

            if not isinstance(taxonomies, dict):
                logger.warning('«{}» config, taxonomies must be a dictionary(key: value)'.format(config_key))
                continue

            for taxonomy_key in taxonomies:
                taxonomy_value = taxonomies[taxonomy_key]

                if not isinstance(taxonomy_value, str) or not isinstance(taxonomy_key, str):
                    logger.warning('«{}» config, taxonomies key and value must be strings'.format(config_key))
                    continue

                if config_key == 'global':
                    self.taxonomies[taxonomy_key] = taxonomy_value
                else:
                    self.taxonomies_by_lang[lang][taxonomy_key] = taxonomy_value

        if not self.taxonomies:
            self.taxonomies = constants.DEFAULT_TAXONOMIES


config = _Config()
