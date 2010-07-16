from django.contrib import admin
from django import forms
from django.contrib.contenttypes import generic

from treenav import models as treenav
from treenav.forms import MenuItemForm, GenericInlineMenuItemForm


class GenericMenuItemInline(generic.GenericStackedInline):
    """
    Add this inline to your admin class to support editing related menu items
    from that model's admin page.
    """
    max_num = 1
    model = treenav.MenuItem
    form = GenericInlineMenuItemForm


class SubMenuItemInline(admin.TabularInline):
    model = treenav.MenuItem
    extra = 1
    form = MenuItemForm
    prepopulated_fields = {'slug': ('label',)}
    exclude = ('new_parent',)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'menu_items',
        'slug',
        'label',
        'parent',
        'link',
        'href_link',
        'order',
        'is_enabled',
    )
    list_filter = ('parent', 'is_enabled')
    raw_id_fields = ('parent',)
    prepopulated_fields = {'slug': ('label',)}
    inlines = (SubMenuItemInline, )
    fieldsets = (
        (None, {
            'fields': ('new_parent', 'label', 'slug', 'order', 'is_enabled')
        }),
        ('URL', {
            'fields': ('link', ('content_type', 'object_id')),
            'description': "Link for this menu item, which can be one of: absolute URL, named URL, or a generic relation using get_absolute_url()"
        }),
    )
    list_editable = ('label',)
    form = MenuItemForm
    
    def menu_items(self, obj):
        if obj.level == 0:
            return obj.label
        return '&nbsp;&nbsp;&nbsp;'*obj.level + '- %s' % obj.label
    menu_items.allow_tags = True
    
    def href_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.href, obj.href)
    href_link.short_description = 'HREF'
    href_link.allow_tags = True

admin.site.register(treenav.MenuItem, MenuItemAdmin)
