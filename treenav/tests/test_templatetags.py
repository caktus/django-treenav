import random
import string

from django.test import TestCase

from treenav.models import MenuItem
from treenav.templatetags.treenav_tags import SingleLevelMenuNode


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

    def test_prepare_template_names_returns_names_for_root_slug(self):
        expected_names = [
            'treenav/root/a.html',
            'treenav/root/menuitem.html',
            'treenav/a.html',
            'treenav/menuitem.html',
        ]

        result = SingleLevelMenuNode('primary-nav', '0')._prepare_template_names(self.root)

        self.assertEqual(result, expected_names)