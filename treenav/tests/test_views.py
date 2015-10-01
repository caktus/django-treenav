from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template.context import Context
from django.template import Template
from django.test import override_settings

from .base import TreeNavTestCase as TestCase
from treenav.context_processors import treenav_active
from treenav.models import MenuItem, Item
from treenav.forms import MenuItemForm
from treenav.tests import Team


@override_settings(ROOT_URLCONF='treenav.tests.urls')
class TreeNavTestCase(TestCase):

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

    def test_treenav_active(self):
        request = HttpRequest()
        request.META['PATH_INFO'] = '/'
        treenav_active(request)

    def test_to_tree(self):
        self.root.to_tree()

    def compile_string(self, url, template_str):
        return Template(template_str).render(Context())

    def test_non_unique_form_save(self):
        dup = MenuItemForm({
            'label': 'test nav',
            'slug': 'primary-nav',
            'order': 0,
        })
        self.assertFalse(dup.is_valid(), 'Form says a duplicate slug is valid.')

    def test_single_level_menu_root(self):
        template_str = """{% load treenav_tags %}
        {% single_level_menu "primary-nav" 0 %}
        """
        result = self.compile_string("/", template_str)
        self.assertNotIn(self.second_level.label, result)

    def test_single_level_menu_about_us(self):
        template_str = """{% load treenav_tags %}
        {% single_level_menu "about-us" 0 %}
        """
        result = self.compile_string("/", template_str)
        self.assertIn(self.second_level.label, result)

    def test_show_treenav(self):
        template_str = """{% load treenav_tags %}
        {% show_treenav "primary-nav" %}
        """
        result = self.compile_string("/", template_str)
        self.assertNotIn(self.second_level.label, result)

    def test_single_level_menu_show_treenav_equality(self):  # necessary?
        """Tests that the single_level_menu and show_treenav tags output the
        same for the top level of the tree.
        """
        template_str = """{% load treenav_tags %}
        {% single_level_menu "primary-nav" 0 %}
        """
        single_level_menu_result = self.compile_string("/", template_str)

        template_str = """{% load treenav_tags %}
        {% show_treenav "primary-nav" %}
        """
        show_treenav_result = self.compile_string("/", template_str)

        self.assertEqual(single_level_menu_result, show_treenav_result)

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
        # FIXME: This fixes the pep8 warning, but need to figure out what we're asserting
        self.assertTrue(compiled)

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
        self.assertEqual(active_item.node, self.child)


@override_settings(ROOT_URLCONF='treenav.tests.urls')
class TreeNavViewTestCase(TestCase):

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
        url = reverse('test_view', args=('home',))
        response = self.client.post(url, {'pslug': 'primary-nav', 'N': 0})
        self.assertEqual(response.content.decode('utf-8').count('<li'), 3)
        self.assertContains(response, 'depth-0')

    def test_tags_no_page(self):
        url = reverse('test_view', args=('notthere',))
        response = self.client.post(url, {'pslug': 'primary-nav', 'N': 0})
        self.assertEqual(response.content.decode('utf-8').count('<li'), 3)
        self.assertContains(response, 'depth-0')

    def test_tags_level2(self):
        self.create_menu_item(
            parent=self.child,
            label='Second Level',
            slug='second-level',
            order=10,
        )
        url = reverse('test_view', args=('home',))
        response = self.client.post(url, {'pslug': 'about-us', 'N': 0})
        self.assertEqual(response.content.decode('utf-8').count('<li'), 1)

    def test_tags_improper(self):
        url = reverse('test_view', args=('home',))
        response = self.client.post(url, {'pslug': 'no-nav', 'N': 10000})
        self.assertNotContains(response, '<ul')

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
        url = reverse('treenav_undefined_url', args=[slug, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


@override_settings(ROOT_URLCONF='treenav.tests.urls')
class RefreshViewTestCase(TestCase):
    "Admin view to trigger refresh of hrefs."

    def setUp(self):
        self.superuser = User.objects.create_user('test', '', 'test')
        self.superuser.is_staff = True
        self.superuser.is_superuser = True
        self.superuser.save()
        self.refresh_url = reverse('admin:treenav_refresh_hrefs')
        self.info = MenuItem._meta.app_label, MenuItem._meta.model_name
        self.changelist_url = reverse('admin:%s_%s_changelist' % self.info)
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

    def test_trigger_refresh_redirects_to_custom_admin(self):
        "Trigger update of menu item HREFs for a second custom admin."
        refresh_url = reverse('admin:treenav_refresh_hrefs',
                              current_app='admin2')
        response = self.client.get(refresh_url, follow=True)
        changelist_url = reverse('admin:%s_%s_changelist' % self.info,
                                 current_app='admin2')
        self.assertRedirects(response, changelist_url)

    def test_no_permission(self):
        "Non-staff cannot trigger the refresh."
        self.superuser.is_staff = False
        self.superuser.save()
        response = self.client.get(self.refresh_url, follow=True)
        # Admin displays a login page with 200 status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['messages']), 0)


@override_settings(ROOT_URLCONF='treenav.tests.urls')
class ClearCacheViewTestCase(TestCase):
    "Admin view to clear menu cache."

    def setUp(self):
        self.superuser = User.objects.create_user('test', '', 'test')
        self.superuser.is_staff = True
        self.superuser.is_superuser = True
        self.superuser.save()
        self.cache_url = reverse('admin:treenav_clean_cache')
        self.info = MenuItem._meta.app_label, MenuItem._meta.model_name
        self.changelist_url = reverse('admin:%s_%s_changelist' % self.info)
        self.client.login(username='test', password='test')

    def test_reset_cache(self):
        "Clear MenuItems from cache."
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

    def test_reset_cache_redirects_to_custom_admin(self):
        "After cleaning cache, redirects to custom admin."
        cache_url = reverse('admin:treenav_clean_cache',
                            current_app='admin2')
        response = self.client.get(cache_url, follow=True)
        changelist_url = reverse('admin:%s_%s_changelist' % self.info,
                                 current_app='admin2')
        self.assertRedirects(response, changelist_url)

    def test_no_permission(self):
        "Non-staff cannot clear the cache."
        self.superuser.is_staff = False
        self.superuser.save()
        response = self.client.get(self.cache_url, follow=True)
        # Admin displays a login page with 200 status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['messages']), 0)


@override_settings(ROOT_URLCONF='treenav.tests.urls')
class SimultaneousReorderTestCase(TestCase):

    def setUp(self):
        self.root = self.create_menu_item(
            label='Primary Navigation',
            slug='primary-nav',
            order=0,
        )
        self.blog = self.create_menu_item(
            parent=self.root,
            label='Our Blog',
            slug='our-blog',
            order=4,
        )
        self.home = self.create_menu_item(
            parent=self.root,
            label='Home',
            slug='home',
            order=0,
        )
        self.superuser = User.objects.create_user('test', '', 'test')
        self.superuser.is_staff = True
        self.superuser.is_superuser = True
        self.superuser.save()
        self.info = MenuItem._meta.app_label, MenuItem._meta.model_name
        self.changeform_url = reverse('admin:%s_%s_change' % self.info, args=(1,))
        self.client.login(username='test', password='test')

    def test_reorder(self):
        # Build up the post dict, starting with the top form
        data = {'parent': '',
                'label': 'Primary Navigation',
                'slug': 'primary-nav',
                'order': 0,
                'is_enabled': 'on',
                'link': '',
                'content_type': '',
                'object_id': ''
                }
        # Now update the post dict with inline form info
        data.update({'children-TOTAL_FORMS': 3,
                     'children-INITIAL_FORMS': 2,
                     'children-MAX_NUM_FORMS': 1000
                     })
        # Update the post dict with the children, swapping their order values
        data.update({'children-0-id': 3,
                     'children-0-parent': 1,
                     'children-0-label': 'Home',
                     'children-0-slug': 'home',
                     'children-0-order': 4,
                     'children-0-is_enabled': 'on',
                     'children-0-link': '',
                     'children-0-content_type': '',
                     'children-0-object_id': '',
                     'children-1-id': 2,
                     'children-1-parent': 1,
                     'children-1-label': 'Our Blog',
                     'children-1-slug': 'our-blog',
                     'children-1-order': 0,
                     'children-1-is_enabled': 'on',
                     'children-1-link': '',
                     'children-1-content_type': '',
                     'children-1-object_id': ''
                     })
        # Update the post dict with the empty inline form entry
        data.update({'children-2-id': '',
                     'children-2-parent': 1,
                     'children-2-label': '',
                     'children-2-slug': '',
                     'children-2-order': '',
                     'children-2-is_enabled': 'on',
                     'children-2-link': '',
                     'children-2-content_type': '',
                     'children-2-object_id': ''
                     })
        # Update the post dict with the end of the form
        data.update({'children-__prefix__-id': '',
                     'children-__prefix__-parent': 1,
                     'children-__prefix__-label': '',
                     'children-__prefix__-slug': '',
                     'children-__prefix__-order': '',
                     'children-__prefix__-is_enabled': 'on',
                     'children-__prefix__-link': '',
                     'children-__prefix__-content_type': '',
                     'children-__prefix__-object_id': '',
                     '_save': 'Save'
                     })
        self.client.post(self.changeform_url, data)
        order = self.root.get_children()
        # Check if children are in the correct order
        self.assertEqual(order[0], self.blog)
        self.assertEqual(order[1], self.home)
        # Check if the lft and rght attributes assigned by mptt are correct
        self.assertNotEqual(order[0].lft, order[1].lft)
        self.assertNotEqual(order[0].rght, order[1].rght)
