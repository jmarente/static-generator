# -*- condig: utf-8 -*-
import os
from time import time
from collections import defaultdict
from sitic.content import Page, Section, Taxonomy, RoutedPage

class _Stats(object):

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.start_time = time()
        self.num_draft = 0
        self.num_expired_rendered = 0
        self.num_expired_removed = 0
        self.num_future = 0
        self.num_pages = 0
        self.num_routed_pages = 0
        self.num_sections = 0
        self.taxonomies_stats = defaultdict(int)

    def get_stats(self):
        result = '{} pages created'.format(self.num_pages) + os.linesep
        result += '{} routed pages created'.format(self.num_routed_pages) + os.linesep
        result += '{} draft content rendered'.format(self.num_draft) + os.linesep
        result += '{} future content rendered'.format(self.num_future) + os.linesep
        result += '{} expired content rendered'.format(self.num_expired_rendered) + os.linesep
        result += '{} expired content removed'.format(self.num_expired_removed) + os.linesep
        result += '{} sections created'.format(self.num_sections) + os.linesep

        for taxonomy in self.taxonomies_stats:
            num = self.taxonomies_stats[taxonomy]
            result += '{} {} taxonomies created'.format(num, taxonomy) + os.linesep

        end_time = round(time() - self.start_time, 3)
        result += 'total in {} seconds'.format(end_time) + os.linesep

        return result

    def update(self, content):
        if isinstance(content, Page):
            self.num_pages += 1
        elif isinstance(content, RoutedPage):
            self.num_routed_pages += 1
        elif isinstance(content, Page) or isinstance(content, RoutedPage):
            if content.draft:
                self.num_draft += 1
            if content.is_expired():
                self.num_expired_rendered += 1
        elif isinstance(content, Section):
            self.num_sections += 1
        elif isinstance(content, Taxonomy):
            self.taxonomies_stats[content.definition.plural] += 1

stats = _Stats()
