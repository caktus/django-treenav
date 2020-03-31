import random
import string
from unittest.mock import ANY, patch

from django.test import TestCase
from django.template import Context, Engine
from django.template.base import Parser, Token, TOKEN_BLOCK

from treenav.models import MenuItem, Item
from treenav.templatetags.treenav_tags import SingleLevelMenuNode, single_level_menu, register


class SingleLevelMenuNodeTestCase(TestCase):
    """TestCase for single_level_menu."""

    def setUp(self):
        self.root = self.create_menu_item(**{
            'label': 'Primary Navigation',
            'slug': 'primary-nav',
            'order': 0,
        })
        self.create_menu_item(**{
            'parent': self.root,
            'label': 'Our Blog',
            'slug': 'our-blog',
            'order': 4,
        })
        self.create_menu_item(**{
            'parent': self.root,
            'label': 'Home',
            'slug': 'home',
            'order': 0,
        })
        self.child = self.create_menu_item(**{
            'parent': self.root,
            'label': 'About Us',
            'slug': 'about-us',
            'order': 9,
        })
        self.second_level = self.create_menu_item(**{
            'parent': self.child,
            'label': 'Second',
            'slug': 'second',
            'order': 0,
        })
        self.third_level = self.create_menu_item(**{
            'parent': self.second_level,
            'label': 'Third',
            'slug': 'third',
            'order': 0,
        })

        self.addCleanup(patch.stopall)
        self.m_render_to_string = patch('treenav.templatetags.treenav_tags.render_to_string').start()

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

    def test_render_to_string_called_with_template_names_for_root_slug(self):
        token = Token(token_type=TOKEN_BLOCK, contents='single_level_menu "primary-nav" 0')
        parser = Parser(tokens=[token], builtins=[register])
        parser.parse()
        node = single_level_menu(parser, token)
        expected_names = [
            # 'treenav/root/a.html',
            # 'treenav/root/menuitem.html',
            'treenav/primary-nav.html',
            'treenav/menuitem.html',
        ]

        node.render_with_args([], 'primary-nav', 0)

        self.m_render_to_string.assert_called_once_with(
            expected_names,
            {'menuitem': ANY, 'full_tree': False, 'single_level': True}
        )

    # def test_prepare_template_names_returns_names_for_first_level_slug(self):
    #     expected_names = [
    #         'treenav/root/about-us/a.html',
    #         'treenav/root/about-us/menuitem.html',
    #         'treenav/root/a.html',
    #         'treenav/root/menuitem.html',
    #         'treenav/a.html',
    #         'treenav/menuitem.html',
    #     ]
    #
    #     # result = SingleLevelMenuNode('about-us', '1')._prepare_template_names(self.child)
    #
    #     self.assertEqual(result, expected_names)
    #
    # def test_prepare_template_names_returns_names_for_second_level_slug(self):
    #     expected_names = [
    #         'treenav/root/about-us/second/a.html',
    #         'treenav/root/about-us/second/menuitem.html',
    #         'treenav/root/about-us/a.html',
    #         'treenav/root/about-us/menuitem.html',
    #         'treenav/root/a.html',
    #         'treenav/root/menuitem.html',
    #         'treenav/a.html',
    #         'treenav/menuitem.html',
    #     ]
    #
    #     # result = SingleLevelMenuNode('second', '2')._prepare_template_names(self.second_level)
    #
    #     self.assertEqual(result, expected_names)
    #
    # def test_prepare_template_names_returns_names_for_third_level_slug(self):
    #     expected_names = [
    #         'treenav/root/about-us/second/third/a.html',
    #         'treenav/root/about-us/second/third/menuitem.html',
    #         'treenav/root/about-us/second/a.html',
    #         'treenav/root/about-us/second/menuitem.html',
    #         'treenav/root/about-us/a.html',
    #         'treenav/root/about-us/menuitem.html',
    #         'treenav/root/a.html',
    #         'treenav/root/menuitem.html',
    #         'treenav/a.html',
    #         'treenav/menuitem.html',
    #     ]
    #
    #     # result = SingleLevelMenuNode('third', '3')._prepare_template_names(self.third_level)
    #
    #     self.assertEqual(result, expected_names)