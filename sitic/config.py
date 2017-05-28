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
    sitemap = None
    rss_limit = constants.DEFAULT_RSS_LIMIT
    description_length = constants.DEFAULT_DESCRIPTION_LENGTH

    def load_config(self, config_file_path):
        self.config_path = config_file_path

        self.base_path = os.path.dirname(os.path.abspath(self.config_path))

        # Default
        self.content_path = os.path.join(self.base_path, constants.DEFAULT_CONTENT_PATH)
        self.public_path = os.path.join(self.base_path, constants.DEFAULT_PUBLIC_PATH)
        self.static_path = os.path.join(self.base_path, constants.DEFAULT_STATIC_PATH)
        self.templates_path = os.path.join(self.base_path, constants.DEFAULT_TEMPLATES_PATH)
        self.locales_path = os.path.join(self.base_path, constants.DEFAULT_LOCALES_PATH)

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

        current_file_path = os.path.abspath(os.path.dirname(__file__))
        self.files_path = os.path.join(current_file_path, 'files/')

    def get_taxonomies(self):
        # TODO make it configurable
        return constants.DEFAULT_TAXONOMIES

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


config = _Config()
