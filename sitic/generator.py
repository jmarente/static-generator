# -*- condig: utf-8 -*-
import os
import shutil

from sitic.config import config
from sitic.content import ContentFactory, Paginator
from sitic.content import MenuBuilder
from sitic.utils import constants
from sitic.template import Render
from sitic.logging import logger
from sitic.content.sitemap import Sitemap
from sitic.scoper import Scoper
from sitic.search_indexer import SearchIndexer
from sitic.content.rss import Rss
from sitic.content.redirect_page import RedirectPage
from sitic.stats import stats

class Generator(object):
    context = {}

    def __init__(self):
        self.content_factory = ContentFactory()
        self.current_url = None
        self.meta_tag = ''

    def build_contents(self):
        self.content_factory.build_contents()

    def gen(self):
        logger.info('Generating site...')

        self.current_url = None

        stats.initialize()
        self.build_contents()
        self.create_public_folder()
        self.move_static_folder()

        self.search_indexer = SearchIndexer()

        for language in config.get_languages():

            # initialize context every loop
            self.context['site'] = {
                'disqus_shortname': config.disqus_shortname,
                'language': language,
                'main_language': config.main_language,
                'languages': config.get_languages_config(),
            }

            render = Render(language)
            sitemap = Sitemap(language)

            contents = self.content_factory.get_contents(language)
            expired_contents = self.content_factory.expired_contents[language]

            taxonomies = self.content_factory.get_taxonomies(language)
            taxonomies_contents = self.get_taxonomies_content(taxonomies)
            sections = self.content_factory.get_sections(language)
            search_page = self.content_factory.search_pages[language]

            self.add_taxonomies_to_context(taxonomies)

            homepage = self.content_factory.homepages[language]
            homepage.pages = contents
            self.context['site']['home_url'] = homepage.get_url()

            rss = self.content_factory.rss[language]

            menu_builder = MenuBuilder(self, contents, sections, language)

            menus = menu_builder.build()
            self.context['site']['menus'] = menus

            all_contents = [homepage] + contents + taxonomies_contents \
                    + sections + rss + [search_page]

            meta_data = {
                'search-index': self.search_indexer.get_url(),
                'language': language,
            }

            self.search_indexer.add_contents(contents + sections)

            meta_values = ['data-{}="{}"'.format(key, value)
                           for key, value in meta_data.items() if value]
            self.meta_tag = '<meta name="sitic" {}/>'.format(' '.join(meta_values))

            for content in all_contents:
                self.current_url = content.get_url()
                stats.update(content)
                self.context['scoper'] = Scoper()
                if content.is_paginable():
                    self.generate_paginable(render, content)
                else:
                    self.generate_regular(render, content)

                # FIXME: temporary fix
                if not isinstance(content, Rss):
                    sitemap.contents.append(content)

                if content.has_redirect_url():
                    all_contents.append(RedirectPage(content.get_redirect_url(), content.get_url()))

            self.generate_regular(render, sitemap)

            self.remove_expired(expired_contents)

        self.search_indexer.create_files()

        logger.info('{}{}{}'.format('Site generated', os.linesep, stats.get_stats()))

    def create_public_folder(self):
        if not os.path.exists(config.public_path):
            os.makedirs(config.public_path)

    def move_static_folder(self):
        if os.path.exists(config.static_path):
            for item in os.listdir(config.static_path):
                origin = os.path.join(config.static_path, item)
                # FIXME: use same name as static source folder
                destination = os.path.join(config.public_path, 'static', item)
                if os.path.isdir(origin):
                    if os.path.exists(destination):
                        shutil.rmtree(destination)
                    shutil.copytree(origin, destination)
                else:
                    shutil.copy2(origin, destination)

    def create_path(self, content_path):
        path = os.path.dirname(content_path)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                pass

    def generate_regular(self, render, content):
        content_path = content.get_path()

        self.create_path(content_path)
        self.context['node'] = content.get_context()
        render.render(content, content_path, self.context, self.meta_tag,
                      self.search_indexer.get_html_includes())

    def generate_paginable(self, render, content):
        page_size = config.paginable or content.pages_count()
        paginator = Paginator(content, page_size)
        self.context['node'] = content.get_context()
        for page_num in paginator.page_range:
            page = paginator.get_page(page_num)
            page_path = page.get_path()

            paginator.page = page

            self.create_path(page_path)
            self.context['node']['paginator'] = paginator
            render.render(content, page_path, self.context, self.meta_tag,
                          self.search_indexer.get_html_includes())

    def remove_expired(self, expired_contents):
        for content in expired_contents:
            content_path = content.get_path()
            # Removes expired content previously published
            if content.is_expired() and os.path.isfile(content_path):
                stats.num_expired_removed += 1
                os.remove(content_path)

    def get_taxonomies_content(self, taxonomies):
        taxonomies_content = []
        for taxonomy in taxonomies.values():
            taxonomies_content += list(taxonomy.values())
        return taxonomies_content

    def add_taxonomies_to_context(self, taxonomies):
        self.context['site']['taxonomies'] = {}
        for plural_definition in taxonomies:
            definition_taxonomies = list(taxonomies[plural_definition].values())
            self.context['site']['taxonomies'][plural_definition] = definition_taxonomies
