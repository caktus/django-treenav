import pprint
import time 

from django.test import TestCase, TransactionTestCase

from treenav.models import MenuItem


class TreeNavTestCase(TransactionTestCase):
    def setUp(self):
        root = MenuItem.objects.create(
            label='Primary Navigation',
            slug='primary-nav',
            order=0,
        )
        MenuItem.objects.create(
            parent=MenuItem.objects.get(slug='primary-nav'),
            label='Our Blog',
            slug='our-blog',
            order=4,
        )
        MenuItem.objects.create(
            parent=MenuItem.objects.get(slug='primary-nav'),
            label='Home',
            slug='home',
            order=0,
        )
        MenuItem.objects.create(
            parent=MenuItem.objects.get(slug='primary-nav'),
            label='About Us',
            slug='about-us',
            order=9,
        )
    
    def testHierarchy(self):
        root = MenuItem.objects.get(slug='primary-nav').to_tree()
        self.assertEqual(len(root.children), 3)
        children = ('Home', 'Our Blog', 'About Us')
        for item, expected_label in zip(root.children, children):
            self.assertEqual(item.node.label, expected_label)
