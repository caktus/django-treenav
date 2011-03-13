from django.db import models
from django.test import TestCase, Client
from django.http import HttpRequest
from django.core.urlresolvers import reverse
from django.template.context import Context
from django.template import compile_string, TemplateSyntaxError, StringOrigin
from django.contrib.contenttypes.models import ContentType

from treenav.context_processors import treenav_active
from treenav.models import MenuItem
from treenav.forms import MenuItemForm

# per http://code.djangoproject.com/ticket/7835#comment:24,
# include test model in tests.py (until there's a better way)
# it does NOT work to include it in a separate file and import it here,
# because the app label will be incorrect.  See:
#   * http://code.djangoproject.com/ticket/4470 (closed as a dup) and
#   * http://code.djangoproject.com/ticket/3591
class Team(models.Model):

    slug = models.SlugField()
    
    def get_absolute_url(self):
        return '/team/%s/' % self.slug


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

    def test_getabsoluteurl(self):
        team = Team.objects.create(slug='durham-bulls')
        ct = ContentType.objects.get(app_label='treenav', model='team')
        form = MenuItemForm({
            'label': 'Durham Bulls',
            'slug': 'durham-bulls',
            'order': 4,
            'content_type': ct.id,
            'object_id': team.pk,
        })
        if not form.is_valid():
            self.fail(form.errors)
        menu = form.save()
        self.assertEqual(menu.href, team.get_absolute_url())
    
    def test_changed_getabsoluteurl(self):
        team = Team.objects.create(slug='durham-bulls')
        ct = ContentType.objects.get(app_label='treenav', model='team')
        menu = MenuItem.objects.create(
            parent=MenuItem.objects.get(slug='primary-nav'),
            label='Durham Bulls',
            slug='durham-bulls',
            order=9,
            content_type=ct,
            object_id=team.pk,
            href=team.get_absolute_url(),
        )
        # change slug and save it to fire post_save signal
        team.slug = 'wildcats'
        team.save()
        menu = MenuItem.objects.get(slug='durham-bulls')
        self.assertEqual(menu.href, team.get_absolute_url())


class TreeNavViewTestCase(TestCase):

    urls = 'treenav.tests.urls'

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
    
    def test_tags_level(self):
        c = Client()
        url = reverse('treenav.tests.urls.test_view',args=('home',))
        response = c.post(url,{'pslug':'primary-nav', 'N':0} )
        self.assertEquals(response.content.count('<li'),3)
        self.assertContains(response,'depth-0')
    
    def test_tags_no_page(self):
        c = Client()
        url = reverse('treenav.tests.urls.test_view',args=('notthere',))
        response = c.post(url,{'pslug':'primary-nav', 'N':0} )
        self.assertEquals(response.content.count('<li'),3)
        self.assertContains(response,'depth-0')
    
    def test_tags_level2(self):
        MenuItem.objects.create(
            parent=MenuItem.objects.get(slug='about-us'),
            label='Second Level',
            slug='second-level',
            order=10,
        )
        c = Client()
        url = reverse('treenav.tests.urls.test_view',args=('home',))
        response = c.post(url,{'pslug':'about-us', 'N':0} )
        self.assertEquals(response.content.count('<li'),1)
        
    def test_tags_improper(self):
        c = Client()
        url = reverse('treenav.tests.urls.test_view',args=('home',))
        response = c.post(url,{'pslug':'no-nav', 'N':10000} )
        self.assertNotContains(response,'<ul')
        
    def test_hierarchy(self):
        root = MenuItem.objects.get(slug='primary-nav').to_tree()
        self.assertEqual(len(root.children), 3)
        children = ('Home', 'Our Blog', 'About Us')
        for item, expected_label in zip(root.children, children):
            self.assertEqual(item.node.label, expected_label)
