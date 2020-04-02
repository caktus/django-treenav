import random
import string
from unittest.mock import ANY, patch

from django.test import TestCase, RequestFactory
from django.template.base import Parser, Token, TOKEN_BLOCK
from django.template.context import make_context

from treenav.models import MenuItem, Item
from treenav.templatetags.treenav_tags import do_render_menu_children, single_level_menu, register


class SingleLevelMenuNodeTestCase(TestCase):
    """TestCase for single_level_menu."""

    def setUp(self):
        self.root = self.create_menu_item(**{
            'label': 'Primary Navigation',
            'slug': 'primary-nav',
            'order': 0,
            'link': '/',
        })
        self.create_menu_item(**{
            'parent': self.root,
            'label': 'Our Blog',
            'slug': 'our-blog',
            'order': 4,
            'link': '/our-blog',
        })
        self.create_menu_item(**{
            'parent': self.root,
            'label': 'Home',
            'slug': 'home',
            'order': 0,
            'link': '/home',
        })
        self.child = self.create_menu_item(**{
            'parent': self.root,
            'label': 'About Us',
            'slug': 'about-us',
            'order': 9,
            'link': '/about-us',
        })
        self.second_level = self.create_menu_item(**{
            'parent': self.child,
            'label': 'Second',
            'slug': 'second',
            'order': 0,
            'link': '/about-us/second',
        })
        self.third_level = self.create_menu_item(**{
            'parent': self.second_level,
            'label': 'Third',
            'slug': 'third',
            'order': 0,
            'link': '/about-us/second/third',
        })

        self.addCleanup(patch.stopall)
        self.m_render_to_string = patch('treenav.templatetags.treenav_tags.render_to_string').start()

        token = Token(token_type=TOKEN_BLOCK, contents='single_level_menu "primary-nav" 0')
        parser = Parser(tokens=[token], builtins=[register])
        parser.parse()
        self.node = single_level_menu(parser, token)

    def create_menu_item(self, **kwargs):
        defaults = {
            'label': self.get_random_string(),
            'slug': self.get_random_string(),
            'order': 0
        }
        defaults.update(kwargs)
        return MenuItem.objects.create(**defaults)

    def get_random_string(self, length=10):
        return ''.join(random.choice(string.ascii_letters) for x in range(length))

    def test_render_to_string_called_with_template_names_for_zero_level(self):
        request = RequestFactory().get('/')
        expected_names = [
            'treenav/primary-nav.html',
            'treenav/menuitem.html',
        ]

        self.node.render_with_args({'request': request}, 'primary-nav', 0)

        self.m_render_to_string.assert_called_once_with(
            expected_names,
            {'request': request, 'active_menu_items': [ANY], 'menuitem': ANY, 'full_tree': False, 'single_level': True}
        )

    def test_render_to_string_called_with_template_names_for_zero_level_even_when_request_path_info_is_deeper(self):
        request = RequestFactory().get('/about-us')
        expected_names = [
            'treenav/primary-nav.html',
            'treenav/menuitem.html',
        ]

        self.node.render_with_args({'request': request}, 'primary-nav', 0)

        self.m_render_to_string.assert_called_once_with(
            expected_names,
            {'request': request, 'active_menu_items': [ANY, ANY], 'menuitem': ANY, 'full_tree': False, 'single_level': True}
        )

    def test_render_to_string_called_with_template_names_for_first_level(self):
        request = RequestFactory().get('/about-us')
        expected_names = [
            'treenav/primary-nav/about-us.html',
            'treenav/primary-nav/menuitem.html',
            'treenav/about-us.html',
            'treenav/menuitem.html',
        ]

        self.node.render_with_args({'request': request}, 'primary-nav', 1)

        self.m_render_to_string.assert_called_once_with(
            expected_names,
            {'request': request, 'active_menu_items': [ANY, ANY], 'menuitem': ANY, 'full_tree': False, 'single_level': True}
        )

    def test_render_to_string_called_with_template_names_for_second_level(self):
        request = RequestFactory().get('/about-us/second')
        expected_names = [
            'treenav/primary-nav/about-us/second.html',
            'treenav/primary-nav/about-us/menuitem.html',
            'treenav/primary-nav/second.html',
            'treenav/primary-nav/menuitem.html',
            'treenav/second.html',
            'treenav/menuitem.html',
        ]

        self.node.render_with_args({'request': request}, 'primary-nav', 2)

        self.m_render_to_string.assert_called_once_with(
            expected_names,
            {'request': request, 'active_menu_items': [ANY, ANY, ANY], 'menuitem': ANY, 'full_tree': False, 'single_level': True}
        )

    def test_render_to_string_called_with_template_names_for_third_level(self):
        request = RequestFactory().get('/about-us/second/third')
        expected_names = [
            'treenav/primary-nav/about-us/second/third.html',
            'treenav/primary-nav/about-us/second/menuitem.html',
            'treenav/primary-nav/about-us/third.html',
            'treenav/primary-nav/about-us/menuitem.html',
            'treenav/primary-nav/third.html',
            'treenav/primary-nav/menuitem.html',
            'treenav/third.html',
            'treenav/menuitem.html',
        ]

        self.node.render_with_args({'request': request}, 'primary-nav', 3)

        self.m_render_to_string.assert_called_once_with(
            expected_names,
            {'request': request, 'active_menu_items': [ANY, ANY, ANY, ANY], 'menuitem': ANY, 'full_tree': False, 'single_level': True}
        )


class DoRenderMenuChildrenTestCase(TestCase):
    """TestCase for do_render_menu_children tag."""

    def setUp(self):
        self.root = self.create_menu_item(**{
            'label': 'Primary Navigation',
            'slug': 'primary-nav',
            'order': 0,
            'link': '/',
        })
        self.create_menu_item(**{
            'parent': self.root,
            'label': 'Our Blog',
            'slug': 'our-blog',
            'order': 4,
            'link': '/our-blog',
        })
        self.create_menu_item(**{
            'parent': self.root,
            'label': 'Home',
            'slug': 'home',
            'order': 0,
            'link': '/home',
        })
        self.child = self.create_menu_item(**{
            'parent': self.root,
            'label': 'About Us',
            'slug': 'about-us',
            'order': 9,
            'link': '/about-us',
        })
        self.second_level = self.create_menu_item(**{
            'parent': self.child,
            'label': 'Second',
            'slug': 'second',
            'order': 0,
            'link': '/about-us/second',
        })
        self.third_level = self.create_menu_item(**{
            'parent': self.second_level,
            'label': 'Third',
            'slug': 'third',
            'order': 0,
            'link': '/about-us/second/third',
        })

        self.addCleanup(patch.stopall)
        self.m_render_to_string = patch('treenav.templatetags.treenav_tags.render_to_string').start()

        token = Token(token_type=TOKEN_BLOCK, contents='render_menu_children item')
        parser = Parser(tokens=[token], builtins=[register])
        parser.parse()
        self.node = do_render_menu_children(parser, token)

    def create_menu_item(self, **kwargs):
        defaults = {
            'label': self.get_random_string(),
            'slug': self.get_random_string(),
            'order': 0
        }
        defaults.update(kwargs)
        return MenuItem.objects.create(**defaults)

    def get_random_string(self, length=10):
        return ''.join(random.choice(string.ascii_letters) for x in range(length))

    def test_render_to_string_called_with_template_names_for_child_level_one(self):
        request = RequestFactory().get('/one')
        root_item = Item(self.root)
        item = Item(self.child)
        context = make_context({
            'request': request,
            'active_menu_items': [root_item, item],
            'menuitem': root_item,
            'full_tree': False,
        })
        context.update({
            'forloop': {
                'parentloop': {},
                'counter0': 0,
                'counter': 1,
                'revcounter': 2,
                'revcounter0': 1,
                'first': True,
                'last': False,
            },
            'item': item,
        })
        expected_names = [
            'treenav/primary-nav/about-us.html',
            'treenav/primary-nav/menuitem.html',
            'treenav/about-us.html',
            'treenav/menuitem.html',
        ]

        self.node.render(context)

        self.m_render_to_string.assert_called_once_with(
            expected_names,
            {'request': request, 'menuitem': item, 'full_tree': False}
        )
