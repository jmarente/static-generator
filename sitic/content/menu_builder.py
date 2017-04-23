# -*- condig: utf-8 -*-
from sitic.config import config
from sitic.logging import logger
from sitic.content.menu import Menu
from sitic.content.page import Page


class MenuBuilder(object):

    def __init__(self, pages = [], sections = []):
        self.pages = pages
        self.sections = sections
        section_pages = [s.content_page for s in sections if s.content_page]
        self.pages = section_pages + self.pages
        self.menus = {}

        self.lazy_menu = config.lazy_menu

    def build(self):
        for page in self.pages:
            self.get_from_page(page)

        self.get_from_config()

        if self.lazy_menu:
            self.build_lazy()

        return self.rank()

    def get_from_page(self, page):
        menus = page.menus()

        if not menus:
            return

        menus_items = menus.items() if isinstance(menus, dict) else enumerate(menus)
        for index, menu_data in menus_items:
            data = self.get_data(index, menu_data)

            if self.lazy_menu and self.lazy_menu == data['name']:
                logger.warning('Menu «{}» declared as lazy menu, skipping for page id «{}»'.format(self.lazy_menu, page.id))
                continue

            if not data:
                continue

            menu_object = self.get_object_from_page(page, data)

            self.add_to_menu(data['name'], menu_object, data.get('parent', None))

    def get_data(self, index, menu_data):
        data = {}
        if isinstance(menu_data, str):
            data['name'] = menu_data
        elif menu_data:
            data = menu_data
            data['name'] = index
        return data

    def get_object_from_page(self, page, menu_data = {}):
        return Menu(
            id=menu_data.get('id', None) or page.id,
            title=menu_data.get('title', None) or page.title,
            weight=menu_data.get('weight', None) or page.weight,
            url=menu_data.get('url', None) or page.get_url()
        )

    def get_object_from_section(self, section):
        return Menu(
            id=section.id,
            title=section.title,
            weight=section.weight,
            url=section.get_url()
        )

    def get_from_config(self):
        menus = config.get_menus()
        for menu_name, items in menus.items():

            for item in items:
                id = item.get('id', None)
                title = item.get('title', None)
                weight = item.get('weight', 0)
                url = item.get('url', None)
                parent = item.get('parent', None)

                if title and id and url:
                    menu_object = Menu(id=id, title=title, weight=weight, url=url)

                    self.add_to_menu(menu_name, menu_object, parent)
                else:
                    logger.warning('Malformed menu item: id, title and url are mandatory')

    def build_lazy(self):
        menu_name = self.lazy_menu

        for section in self.sections:
            section_menu_object = self.get_object_from_section(section)
            section_id = section_menu_object.id

            self.add_to_menu(menu_name, section_menu_object)
            for page in section.pages:

                menu_object = self.get_object_from_page(page)

                self.add_to_menu(menu_name, menu_object, section_id)

    def rank(self):
        for menu_name, menu_items in self.menus.items():
            for key, menu in menu_items.items():
                parent_id = menu['parent_id']
                menu_object = menu['object']

                if parent_id in menu_items:
                    parent_object = menu_items[parent_id]['object']
                    parent_object.add_children(menu_object)

        formatted_menus = {}
        for menu_name, menu_items in self.menus.items():

            without_parents = [x['object'] for x in menu_items.values() if x['object'].parent is None]
            formatted_menus[menu_name] = sorted(without_parents, key = lambda x: x.weight)

        return formatted_menus

    def add_to_menu(self, menu_name, menu_object, parent=None):
        if menu_name not in self.menus:
            self.menus[menu_name] = {}

        menu_id = menu_object.id
        if menu_id in self.menus[menu_name]:
            logger.warning('Duplicated menu element found for id «{}»'.format(menu_id))

        self.menus[menu_name][menu_id] = {
            'object': menu_object,
            'parent_id': parent
        }
