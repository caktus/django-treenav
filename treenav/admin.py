from django.contrib import admin

from treenav import models as treenav
from treenav.forms import MenuItemForm


class SubMenuItemInline(admin.TabularInline):
    model = treenav.MenuItem
    extra = 1
    form = MenuItemForm
    prepopulated_fields = {'slug': ('label',)}
    exclude = ('new_parent',)


class MenuItemAdmin(admin.ModelAdmin):
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
    ordering = ('-parent', 'order',)
    list_editable = ('label',)
    form = MenuItemForm
    
    def href_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.href, obj.href)
    href_link.short_description = 'HREF'
    href_link.allow_tags = True

admin.site.register(treenav.MenuItem, MenuItemAdmin)
