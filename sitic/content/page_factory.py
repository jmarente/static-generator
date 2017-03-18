# -*- condig: utf-8 -*-
import os

from sitic.config import config
from sitic.content import Page, page_parser


class PageFactory(object):

    def get_pages(self, pages_path):
        return [self.get_page(path) for path in pages_path]

    def get_page(self, page_path):
        frontmatter, content = page_parser.load(page_path)

        relative_path = page_path.replace(config.content_path, "").strip(os.sep)
        path_chunks = relative_path.split(os.sep)
        name = path_chunks[-1]
        sections = []
        if len(path_chunks) > 1:
            sections = path_chunks[:-1]

        return Page(frontmatter, content, name, sections)
