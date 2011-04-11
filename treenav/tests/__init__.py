from django.db import models, transaction
from django.test import TestCase, Client, TransactionTestCase
from django.http import HttpRequest
from django.core.urlresolvers import reverse
from django.template.context import Context
from django.template import compile_string, TemplateSyntaxError, StringOrigin
from django.contrib.contenttypes.models import ContentType

from treenav.context_processors import treenav_active
from treenav.models import MenuItem, Item
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


class TreeOrder(TransactionTestCase):
    """
    Test checking that if children added out of order to a new tree will be
    ordered properly when called.
    The original source of this bug is django-mptt but this does check that menu
    item is ordering by the correct attributes as well.
    https://github.com/django-mptt/django-mptt/issues#issue/14
    """

    def test_order(self):
        primary_nav = MenuItem(
            label='primary-nav',
            slug='primary-nav',
            order=0,
            )
        primary_nav.save()
        child = {}
        for i in [2,4,5,1,0,8]:
            child[i] = MenuItem(
                parent=primary_nav,
                label=str(i),
                slug=str(i),
                order=i,
                link='/',
                )
            child[i].save()
        order = MenuItem.objects.exclude(
            slug='primary-nav'
            ).values_list('order', flat=True)
        self.assertEquals(list(order), sorted(order))


class TreeNavTestCase(TestCase):

    urls = 'treenav.tests.urls'

    def setUp(self):
        form = MenuItemForm({
            'label': 'Primary Navigation',
            'slug': 'primary-nav',
            'order': 0,
        })
        self.root = form.save()
        MenuItemForm({
            'parent': MenuItem.objects.get(slug='primary-nav').pk,
            'label': 'Our Blog',
            'slug': 'our-blog',
            'order': 4,
        }).save()
        MenuItemForm({
            'parent': MenuItem.objects.get(slug='primary-nav').pk,
            'label': 'Home',
            'slug': 'home',
            'order': 0,
        }).save()
        self.child = MenuItemForm({
            'parent': MenuItem.objects.get(slug='primary-nav').pk,
            'label': 'Abot Us',
            'slug': 'about-us',
            'order': 9,
        }).save()


    def test_treenav_active(self):
        request = HttpRequest()
        request.META['PATH_INFO'] = '/'
        treenav_active(request)

    def test_to_tree(self):
        self.root.to_tree()

    def compile_string(self, url, template_str):
        origin = StringOrigin(url)
        return compile_string(template_str, origin).render(Context())

    def test_non_unique_form_save(self):
        dup = MenuItemForm({
            'label': 'test nav',
            'slug': 'primary-nav',
            'order': 0,
        })
        self.assertFalse(dup.is_valid(), 'Form says a duplicate slug is valid.')

    def test_single_level_menu(self):
        template_str = """{% load treenav_tags %}
        {% single_level_menu "primary-nav" 0 %}
        """
        self.compile_string("/", template_str)

    def test_show_treenav(self):
        template_str = """{% load treenav_tags %}
        {% show_treenav "primary-nav" %}
        """
        self.compile_string("/", template_str)

    def test_show_menu_crumbs(self):
        template_str = """{% load treenav_tags %}
        {% show_menu_crumbs "about-us" %}
        """
        team = Team.objects.create(slug='durham-bulls')
        ct = ContentType.objects.get(app_label='treenav', model='team')
        form = MenuItemForm({
            'parent': MenuItem.objects.get(slug='primary-nav').pk,
            'label': 'Durham Bulls',
            'slug': 'durham-bulls',
            'order': 4,
            'content_type': ct.id,
            'object_id': team.pk,
        })
        form.save()
        compiled = self.compile_string(team.get_absolute_url(), template_str)


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

    def test_active_url(self):
        team = Team.objects.create(slug='durham-bulls')
        ct = ContentType.objects.get(app_label='treenav', model='team')
        self.child.object_id = team.pk
        self.child.content_type = ct
        self.child.content_object = team
        self.child.save()
        item = Item(self.child)
        active_item = item.set_active(team.get_absolute_url())
        self.assertEquals(active_item.node, self.child)


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
        self.child = MenuItem.objects.create(
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

    def test_undefined_url(self):
        """
        Testing the undefined_url view.
        """
        slug = self.child.slug
        url = reverse('treenav_undefined_url', args=[slug,])
        c = Client()
        response = c.get(url)
        self.assertEquals(response.status_code, 404)

