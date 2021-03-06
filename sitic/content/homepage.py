# -*- condig: utf-8 -*-
from sitic.content.paginable_content import PaginableContent


class Homepage(PaginableContent):

    def __init__(self, language):
        super(Homepage, self).__init__()
        self.name = 'Homepage'
        self.language = language

    def set_content_page(self, page):
        self.content_page = page

    def _get_url(self):
        return '/'

    def get_templates(self):
        return [
            "index.html",
            "default/list.html",
            "default/page.html",
        ]
