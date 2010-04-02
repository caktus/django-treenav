from django.test import TestCase, Client
from django.http import HttpRequest
from django.template.context import Context
from django.template import compile_string, TemplateSyntaxError, StringOrigin

from treenav.context_processors import treenav_active
from treenav.models import MenuItem

class TreeNavTestCase(TestCase):
    def setUp(self):
        self.root = MenuItem.objects.create(
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
    
    def test_treenav_active(self):
        request = HttpRequest()
        request.META['PATH_INFO'] = '/'
        treenav_active(request)
        
    def test_to_tree(self):
        self.root.to_tree()
        
    def test_single_level_menu(self):    
        template_str = """{% load treenav_tags %}
        {% single_level_menu "primary-nav" 0 %}
        """
        origin = StringOrigin('/')
        compiled = compile_string(template_str, origin).render(Context())
        
    def test_show_treenav(self):    
        template_str = """{% load treenav_tags %}
        {% show_treenav "primary-nav" %}
        """
        origin = StringOrigin('/')
        compiled = compile_string(template_str, origin).render(Context())
