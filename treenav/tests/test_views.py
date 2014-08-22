from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template.context import Context
from django.template import compile_string, TemplateSyntaxError, StringOrigin

from .base import TreeNavTestCase as TestCase
from treenav.context_processors import treenav_active
from treenav.models import MenuItem, Item
from treenav.forms import MenuItemForm
from treenav.tests import Team


class TreeNavTestCase(TestCase):

    urls = 'treenav.tests.urls'

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
        second_level = self.create_menu_item(**{
            'parent': self.child,
            'label': 'Second',
            'slug': 'second',
            'order': 0,
        })
        self.third_level = self.create_menu_item(**{
            'parent': second_level,
            'label': 'Third',
            'slug': 'third',
            'order': 0,
        })

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

    def test_show_treenav_third_level(self):
        template_str = """{% load treenav_tags %}
        {% show_treenav "primary-nav" full_tree="True" %}
        """
        result = self.compile_string("/", template_str)
        self.assertIn(self.third_level.label, result)

    def test_show_menu_crumbs(self):
        template_str = """{% load treenav_tags %}
        {% show_menu_crumbs "about-us" %}
        """
        team = Team.objects.create(slug='durham-bulls')
        ct = ContentType.objects.get(app_label='treenav', model='team')
        self.create_menu_item(**{
            'parent': self.root,
            'label': 'Durham Bulls',
            'slug': 'durham-bulls',
            'order': 4,
            'content_type': ct,
            'object_id': team.pk,
        })
        compiled = self.compile_string(team.get_absolute_url(), template_str)

    def test_getabsoluteurl(self):
        team = Team.objects.create(slug='durham-bulls')
        ct = ContentType.objects.get(app_label='treenav', model='team')
        menu = self.create_menu_item(**{
            'label': 'Durham Bulls',
            'slug': 'durham-bulls',
            'order': 4,
            'content_type': ct,
            'object_id': team.pk,
        })
        self.assertEqual(menu.href, team.get_absolute_url())

    def test_changed_getabsoluteurl(self):
        team = Team.objects.create(slug='durham-bulls')
        ct = ContentType.objects.get(app_label='treenav', model='team')
        menu = self.create_menu_item(
            parent=self.root,
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
        self.root = self.create_menu_item(
            label='Primary Navigation',
            slug='primary-nav',
            order=0,
        )
        self.create_menu_item(
            parent=self.root,
            label='Our Blog',
            slug='our-blog',
            order=4,
        )
        self.create_menu_item(
            parent=self.root,
            label='Home',
            slug='home',
            order=0,
        )
        self.child = self.create_menu_item(
            parent=self.root,
            label='About Us',
            slug='about-us',
            order=9,
        )

    def test_tags_level(self):
        url = reverse('treenav.tests.urls.test_view',args=('home',))
        response = self.client.post(url,{'pslug':'primary-nav', 'N':0} )
        self.assertEquals(response.content.count('<li'),3)
        self.assertContains(response,'depth-0')

    def test_tags_no_page(self):
        url = reverse('treenav.tests.urls.test_view',args=('notthere',))
        response = self.client.post(url,{'pslug':'primary-nav', 'N':0} )
        self.assertEquals(response.content.count('<li'),3)
        self.assertContains(response,'depth-0')

    def test_tags_level2(self):
        self.create_menu_item(
            parent=self.child,
            label='Second Level',
            slug='second-level',
            order=10,
        )
        url = reverse('treenav.tests.urls.test_view',args=('home',))
        response = self.client.post(url,{'pslug':'about-us', 'N':0} )
        self.assertEquals(response.content.count('<li'),1)

    def test_tags_improper(self):
        url = reverse('treenav.tests.urls.test_view',args=('home',))
        response = self.client.post(url,{'pslug':'no-nav', 'N':10000} )
        self.assertNotContains(response,'<ul')

    def test_hierarchy(self):
        root = self.root.to_tree()
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
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)


class RefreshViewTestCase(TestCase):
    "Admin view to trigger refresh of hrefs."

    urls = 'treenav.tests.urls'

    def setUp(self):
        self.superuser = User.objects.create_user('test', '', 'test')
        self.superuser.is_staff = True
        self.superuser.is_superuser = True
        self.superuser.save()
        self.refresh_url = reverse('admin:treenav_refresh_hrefs')
        info = MenuItem._meta.app_label, MenuItem._meta.module_name
        self.changelist_url = reverse('admin:%s_%s_changelist' % info)
        self.client.login(username='test', password='test')

    def test_trigger_refresh(self):
        "Trigger update of menu item HREFs."
        team = Team.objects.create(slug='durham-bulls')
        ct = ContentType.objects.get(app_label='treenav', model='team')
        menu = self.create_menu_item(
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
        self.assertNotEqual(menu.href, team.get_absolute_url())
        response = self.client.get(self.refresh_url, follow=True)
        self.assertRedirects(response, self.changelist_url)
        menu = MenuItem.objects.get(pk=menu.pk)
        self.assertEqual(menu.href, team.get_absolute_url())
        self.assertEqual(len(response.context['messages']), 1)

    def test_no_permission(self):
        "Non-staff cannot trigger the refresh."
        self.superuser.is_staff = False
        self.superuser.save()
        response = self.client.get(self.refresh_url, follow=True)
        # Admin displays a login page with 200 status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['messages']), 0)


class ClearCacheViewTestCase(TestCase):
    "Admin view to clear menu cache."

    urls = 'treenav.tests.urls'

    def setUp(self):
        self.superuser = User.objects.create_user('test', '', 'test')
        self.superuser.is_staff = True
        self.superuser.is_superuser = True
        self.superuser.save()
        self.cache_url = reverse('admin:treenav_clean_cache')
        info = MenuItem._meta.app_label, MenuItem._meta.module_name
        self.changelist_url = reverse('admin:%s_%s_changelist' % info)
        self.client.login(username='test', password='test')

    def test_reset_cache(self):
        "Trigger update of menu item HREFs."
        menu = self.create_menu_item(
            label='Our Blog',
            slug='our-blog',
            order=4,
        )
        menu.to_tree()
        valid = cache.get('menu-tree-%s' % menu.slug)
        self.assertTrue(valid, 'Menu should be cached')
        cache.set('menu-tree-%s' % menu.slug, 'INVALID!!!')
        response = self.client.get(self.cache_url, follow=True)
        self.assertRedirects(response, self.changelist_url)
        self.assertEqual(len(response.context['messages']), 1)
        # Cache should be recycled
        current = cache.get('menu-tree-%s' % menu.slug)
        self.assertNotEqual(current, 'INVALID!!!')

    def test_no_permission(self):
        "Non-staff cannot clear the cache."
        self.superuser.is_staff = False
        self.superuser.save()
        response = self.client.get(self.cache_url, follow=True)
        # Admin displays a login page with 200 status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['messages']), 0)
