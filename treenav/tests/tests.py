from django.test import TestCase, Client
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from django.http import HttpRequest
from treenav.models import MenuItem
from treenav.forms import MenuItemForm

from treenav.tests.models import Team


class TreeNavTestCase(TestCase):
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
    
    def testTagsLevel(self):
        c = Client()
        url = reverse('treenav.tests.urls.test_view',args=('home',))
        response = c.post(url,{'pslug':'primary-nav', 'N':0} )
        self.assertEquals(response.content.count('<li'),3)
        self.assertContains(response,'depth-0')
    
    def testTagsNoPage(self):
        c = Client()
        url = reverse('treenav.tests.urls.test_view',args=('notthere',))
        response = c.post(url,{'pslug':'primary-nav', 'N':0} )
        self.assertEquals(response.content.count('<li'),3)
        self.assertContains(response,'depth-0')
    
    def testTagsLevel2(self):
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
        
    def testTagsImProper(self):
        c = Client()
        url = reverse('treenav.tests.urls.test_view',args=('home',))
        response = c.post(url,{'pslug':'no-nav', 'N':10000} )
        self.assertNotContains(response,'<ul')
        
    def testHierarchy(self):
        root = MenuItem.objects.get(slug='primary-nav').to_tree()
        self.assertEqual(len(root.children), 3)
        children = ('Home', 'Our Blog', 'About Us')
        for item, expected_label in zip(root.children, children):
            self.assertEqual(item.node.label, expected_label)
    
    def testGetAbsoluteUrl(self):
        team = Team.objects.create(slug='durham-bulls')
        ct = ContentType.objects.get(app_label='tests', model='team')
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
    
    def testChangedGetAbsoluteUrl(self):
        team = Team.objects.create(slug='durham-bulls')
        ct = ContentType.objects.get(app_label='tests', model='team')
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
