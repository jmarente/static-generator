# -*- condig: utf-8 -*-
from sitic.content.base_content import BaseContent


class SearchPage(BaseContent):

    indexable = False

    def __init__(self, language):
        super(SearchPage, self).__init__()
        self.name = 'Search'
        self.language = language

    def _get_url(self):
        return '/search'

    def get_templates(self):
        return ["search.html"]
