from functools import update_wrapper
from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.admin import GenericStackedInline
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from mptt.admin import MPTTModelAdmin

from treenav import models as treenav
from treenav.forms import MenuItemForm, MenuItemInlineForm, GenericInlineMenuItemForm


class GenericMenuItemInline(GenericStackedInline):
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
        urls = [
            url(r'^refresh-hrefs/$', wrap(self.refresh_hrefs), name='treenav_refresh_hrefs'),
            url(r'^clean-cache/$', wrap(self.clean_cache), name='treenav_clean_cache'),
            url(r'^rebuild-tree/$', wrap(self.rebuild_tree), name='treenav_rebuild_tree')
        ] + urls
        return urls

    def refresh_hrefs(self, request):
        """
        Refresh all the cached menu item HREFs in the database.
        """
        for item in treenav.MenuItem.objects.all():
            item.save()  # refreshes the HREF
        self.message_user(request, _('Menu item HREFs refreshed successfully.'))
        info = self.model._meta.app_label, self.model._meta.model_name
        changelist_url = reverse('admin:%s_%s_changelist' % info, current_app=self.admin_site.name)
        return redirect(changelist_url)

    def clean_cache(self, request):
        """
        Remove all MenuItems from Cache.
        """
        treenav.delete_cache()
        self.message_user(request, _('Cache menuitem cache cleaned successfully.'))
        info = self.model._meta.app_label, self.model._meta.model_name
        changelist_url = reverse('admin:%s_%s_changelist' % info, current_app=self.admin_site.name)
        return redirect(changelist_url)

    def rebuild_tree(self, request):
        '''
        Rebuilds the tree and clears the cache.
        '''
        self.model.objects.rebuild()
        self.message_user(request, _('Menu Tree Rebuilt.'))
        return self.clean_cache(request)

    def save_related(self, request, form, formsets, change):
        """
        Rebuilds the tree after saving items related to parent.
        """
        super(MenuItemAdmin, self).save_related(request, form, formsets, change)
        self.model.objects.rebuild()


admin.site.register(treenav.MenuItem, MenuItemAdmin)
