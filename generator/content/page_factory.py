# -*- condig: utf-8 -*-
from generator.config import config
from generator.content import Page, page_parser


class PageFactory(object):

    def get_pages(self, pages_path):
        return [self.get_page(path) for path in pages_path]

    def get_page(self, page_path):
        frontmatter, content = page_parser.load(page_path)
        return Page(frontmatter, content)
