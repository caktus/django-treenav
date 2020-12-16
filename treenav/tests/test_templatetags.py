from unittest.mock import ANY, patch

from django.template.base import Parser, Token, TokenType
from django.template.context import make_context
from django.test import RequestFactory, TestCase, tag

from treenav.models import Item, MenuItem
from treenav.templatetags.treenav_tags import (
    do_render_menu_children,
    register,
    show_treenav,
    single_level_menu,
)


@tag("unit")
class CaktNodeTestCase(TestCase):
    """TestCase for CaktNode."""

    pass


@tag("unit")
class SingleLevelMenuNodeTestCase(TestCase):
    """TestCase for single_level_menu."""

    @classmethod
    def setUpTestData(cls):
        cls.root = MenuItem.objects.create(
            **{
                "label": "Primary Navigation",
                "slug": "primary-nav",
                "order": 0,
                "link": "/",
            }
        )
        cls.child = MenuItem.objects.create(
            **{
                "parent": cls.root,
                "label": "About Us",
                "slug": "about-us",
                "order": 9,
                "link": "/about-us",
            }
        )
        cls.second_level = MenuItem.objects.create(
            **{
                "parent": cls.child,
                "label": "Second",
                "slug": "second",
                "order": 0,
                "link": "/about-us/second",
            }
        )
        cls.third_level = MenuItem.objects.create(
            **{
                "parent": cls.second_level,
                "label": "Third",
                "slug": "third",
                "order": 0,
                "link": "/about-us/second/third",
            }
        )
        token = Token(
            token_type=TokenType.BLOCK, contents='single_level_menu "primary-nav" 0'
        )
        parser = Parser(tokens=[token], builtins=[register])
        parser.parse()
        cls.node = single_level_menu(parser, token)

    def setUp(self):
        self.addCleanup(patch.stopall)
        self.m_render_to_string = patch(
            "treenav.templatetags.treenav_tags.render_to_string"
        ).start()

    def test_render_to_string_called_with_template_names_for_zero_level(self):
        request = RequestFactory().get("/")
        context = make_context({"request": request})
        expected_names = [
            "treenav/primary-nav.html",
            "treenav/menuitem.html",
        ]
        expected_context = {
            "request": request,
            "active_menu_items": [ANY],
            "menuitem": ANY,
            "full_tree": False,
            "single_level": True,
        }

        self.node.render_with_args(context, "primary-nav", 0)

        self.m_render_to_string.assert_called_once_with(
            expected_names, expected_context
        )

    def test_render_to_string_called_with_template_names_for_zero_level_even_when_request_path_info_is_deeper(
        self,
    ):
        request = RequestFactory().get("/about-us")
        expected_names = [
            "treenav/primary-nav.html",
            "treenav/menuitem.html",
        ]
        expected_context = {
            "request": request,
            "active_menu_items": [ANY, ANY],
            "menuitem": ANY,
            "full_tree": False,
            "single_level": True,
        }

        self.node.render_with_args({"request": request}, "primary-nav", 0)

        self.m_render_to_string.assert_called_once_with(
            expected_names, expected_context
        )

    def test_render_to_string_called_with_template_names_for_first_level(self):
        request = RequestFactory().get("/about-us")
        expected_names = [
            "treenav/primary-nav/about-us.html",
            "treenav/primary-nav/menuitem.html",
            "treenav/about-us.html",
            "treenav/menuitem.html",
        ]
        expected_context = {
            "request": request,
            "active_menu_items": [ANY, ANY],
            "menuitem": ANY,
            "full_tree": False,
            "single_level": True,
        }

        self.node.render_with_args({"request": request}, "primary-nav", 1)

        self.m_render_to_string.assert_called_once_with(
            expected_names, expected_context
        )

    def test_render_to_string_called_with_template_names_for_second_level(self):
        request = RequestFactory().get("/about-us/second")
        expected_names = [
            "treenav/primary-nav/about-us/second.html",
            "treenav/primary-nav/about-us/menuitem.html",
            "treenav/primary-nav/second.html",
            "treenav/primary-nav/menuitem.html",
            "treenav/second.html",
            "treenav/menuitem.html",
        ]
        expected_context = {
            "request": request,
            "active_menu_items": [ANY, ANY, ANY],
            "menuitem": ANY,
            "full_tree": False,
            "single_level": True,
        }

        self.node.render_with_args({"request": request}, "primary-nav", 2)

        self.m_render_to_string.assert_called_once_with(
            expected_names, expected_context
        )

    def test_render_to_string_called_with_template_names_for_third_level(self):
        request = RequestFactory().get("/about-us/second/third")
        expected_names = [
            "treenav/primary-nav/about-us/second/third.html",
            "treenav/primary-nav/about-us/second/menuitem.html",
            "treenav/primary-nav/about-us/third.html",
            "treenav/primary-nav/about-us/menuitem.html",
            "treenav/primary-nav/third.html",
            "treenav/primary-nav/menuitem.html",
            "treenav/third.html",
            "treenav/menuitem.html",
        ]
        expected_context = {
            "request": request,
            "active_menu_items": [ANY, ANY, ANY, ANY],
            "menuitem": ANY,
            "full_tree": False,
            "single_level": True,
        }

        self.node.render_with_args({"request": request}, "primary-nav", 3)

        self.m_render_to_string.assert_called_once_with(
            expected_names, expected_context
        )


@tag("unit")
class DoRenderMenuChildrenTestCase(TestCase):
    """TestCase for do_render_menu_children tag."""

    @classmethod
    def setUpTestData(cls):
        cls.root = MenuItem.objects.create(
            **{
                "label": "Primary Navigation",
                "slug": "primary-nav",
                "order": 0,
                "link": "/",
            }
        )
        cls.child = MenuItem.objects.create(
            **{
                "parent": cls.root,
                "label": "About Us",
                "slug": "about-us",
                "order": 0,
                "link": "/about-us",
            }
        )

        token = Token(token_type=TokenType.BLOCK, contents="render_menu_children item")
        parser = Parser(tokens=[token], builtins=[register])
        parser.parse()
        cls.node = do_render_menu_children(parser, token)

    def setUp(self):
        self.addCleanup(patch.stopall)
        self.m_render_to_string = patch(
            "treenav.templatetags.treenav_tags.render_to_string"
        ).start()

        self.request = RequestFactory().get("/one")
        self.root_item = Item(self.root)
        self.child_item = Item(self.child)
        self.context = make_context(
            {
                "request": self.request,
                "active_menu_items": [self.root_item, self.child_item],
                "menuitem": self.root_item,
                "full_tree": True,
            }
        )

    def test_render_to_string_called_with_template_names_for_child_level_one(self):
        self.context.update(
            {
                "forloop": {
                    "parentloop": {},
                    "counter0": 0,
                    "counter": 1,
                    "revcounter": 2,
                    "revcounter0": 1,
                    "first": True,
                    "last": False,
                },
                "item": self.child_item,
            }
        )
        expected_names = [
            "treenav/primary-nav/about-us.html",
            "treenav/primary-nav/menuitem.html",
            "treenav/about-us.html",
            "treenav/menuitem.html",
        ]

        self.node.render(self.context)

        self.m_render_to_string.assert_called_once_with(expected_names, ANY)

    def test_render_to_string_called_with_updated_context(self):
        self.context.update(
            {
                "forloop": {
                    "parentloop": {},
                    "counter0": 0,
                    "counter": 1,
                    "revcounter": 2,
                    "revcounter0": 1,
                    "first": True,
                    "last": False,
                },
                "item": self.child_item,
            }
        )
        expected_context = {
            "request": self.request,
            "menuitem": self.child_item,
            "full_tree": True,
        }

        self.node.render(self.context)

        self.m_render_to_string.assert_called_once_with(ANY, expected_context)


@tag("unit")
class ShowTreenavTestCase(TestCase):
    """TestCase for show_treenav tag."""

    @classmethod
    def setUpTestData(cls):
        cls.root = MenuItem.objects.create(
            **{
                "label": "Primary Navigation",
                "slug": "primary-nav",
                "order": 0,
                "link": "/",
            }
        )
        cls.child = MenuItem.objects.create(
            **{
                "parent": cls.root,
                "label": "About Us",
                "slug": "about-us",
                "order": 0,
                "link": "/about-us",
            }
        )

        token = Token(token_type=TokenType.BLOCK, contents='show_treenav "primary-nav"')
        parser = Parser(tokens=[token], builtins=[register])
        parser.parse()
        cls.node = show_treenav(parser, token)

    def setUp(self):
        self.addCleanup(patch.stopall)
        self.m_render_to_string = patch(
            "treenav.templatetags.treenav_tags.render_to_string"
        ).start()

        self.request = RequestFactory().get("/")
        self.context = make_context({"request": self.request})

    def test_render_to_string_called_with_template_names_for_root_item(self):
        expected_names = [
            "treenav/primary-nav.html",
            "treenav/menuitem.html",
        ]
        expected_context = {
            "request": self.request,
            "active_menu_items": [ANY],
            "menuitem": ANY,
            "full_tree": False,
        }

        self.node.render_with_args(self.context, "primary-nav")

        self.m_render_to_string.assert_called_once_with(
            expected_names, expected_context
        )

    def test_render_to_string_called_with_updated_context(self):
        expected_context = {
            "request": self.request,
            "active_menu_items": [ANY],
            "menuitem": ANY,
            "full_tree": True,
        }

        self.node.render_with_args(self.context, "primary-nav", "True")

        self.m_render_to_string.assert_called_once_with(ANY, expected_context)
