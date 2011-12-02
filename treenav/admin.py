from django.contrib import admin
from django.contrib.contenttypes import generic

from mptt.admin import MPTTModelAdmin

from treenav import models as treenav
from treenav.forms import MenuItemForm, GenericInlineMenuItemForm


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
    form = MenuItemForm
    prepopulated_fields = {'slug': ('label',)}


class MenuItemAdmin(MPTTModelAdmin):
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

admin.site.register(treenav.MenuItem, MenuItemAdmin)
