from functools import update_wrapper
try:
    from django.conf.urls import patterns, url
except ImportError:
    # Django <= 1.3
    from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from mptt.admin import MPTTModelAdmin

from treenav import models as treenav
from treenav.forms import MenuItemForm, MenuItemInlineForm, GenericInlineMenuItemForm


class GenericMenuItemInline(generic.GenericStackedInline):
    """
    Add this inline to your admin class to support editing related menu items
    from that model's admin page.
    """
    extra = 0
    max_num = 1
    model = treenav.MenuItem
    form = GenericInlineMenuItemForm


class SubMenuItemInline(admin.TabularInline):
    model = treenav.MenuItem
    extra = 1
    form = MenuItemInlineForm
    prepopulated_fields = {'slug': ('label',)}


class MenuItemAdmin(MPTTModelAdmin):
    change_list_template = 'admin/treenav/menuitem/change_list.html'
    list_display = (
        'slug',
        'label',
        'parent',
        'link',
        'href_link',
        'order',
        'is_enabled',
    )
    list_filter = ('parent', 'is_enabled')
    prepopulated_fields = {'slug': ('label',)}
    inlines = (SubMenuItemInline,)
    fieldsets = (
        (None, {
            'fields': ('parent', 'label', 'slug', 'order', 'is_enabled')
        }),
        ('URL', {
            'fields': ('link', ('content_type', 'object_id')),
            'description': "The URL for this menu item, which can be a "
                           "fully qualified URL, an absolute URL, a named "
                           "URL, a path to a Django view, a regular "
                           "expression, or a generic relation to a model that "
                           "supports get_absolute_url()"
        }),
    )
    list_editable = ('label',)
    form = MenuItemForm
    
    def href_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.href, obj.href)
    href_link.short_description = 'HREF'
    href_link.allow_tags = True

    def get_urls(self):
        urls = super(MenuItemAdmin, self).get_urls()
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        urls = patterns('',
            url(r'^refresh-hrefs/$', wrap(self.refresh_hrefs), name='treenav_refresh_hrefs'),
            url(r'^clean-cache/$', wrap(self.clean_cache), name='treenav_clean_cache'),
        ) + urls
        return urls

    def refresh_hrefs(self, request):
        """
        Refresh all the cached menu item HREFs in the database.
        """
        for item in treenav.MenuItem.objects.all():
            item.save() # refreshes the HREF
        self.message_user(request, _('Menu item HREFs refreshed successfully.'))
        info = self.model._meta.app_label, self.model._meta.module_name
        return redirect('admin:%s_%s_changelist' % info)

    def clean_cache(self, request):
        """
        Remove all MenuItems from Cache.
        """
        treenav.delete_cache()
        self.message_user(request, _('Cache menuitem cache cleaned successfully.'))
        info = self.model._meta.app_label, self.model._meta.module_name
        return redirect('admin:%s_%s_changelist' % info)


admin.site.register(treenav.MenuItem, MenuItemAdmin)
