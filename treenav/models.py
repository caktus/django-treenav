import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django.core.cache import cache
from django.core.urlresolvers import reverse

from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from mptt.utils import previous_current_next
from mptt.querysets import TreeQuerySet


class Item(object):
    def __init__(self, node):
        self.parent = None
        self.node = node
        self.children = []
        self.active = False

    def __repr__(self):
        return str(self.node)

    def add_child(self, item):
        if hasattr(self, '_enabled_children'):
            del self._enabled_children
        item.parent = self
        self.children.append(item)

    @property
    def enabled_children(self):
        children = getattr(self, '_enabled_children', None)
        if children is None:
            children = [c for c in self.children if c.node.is_enabled]
            self._enabled_children = children
        return children

    def set_active(self, href):
        active_node = None
        if (self.node.href.startswith('^') and re.match(self.node.href, href)) or self.node.href == href:
            self.active = True
            parent = self.parent
            while parent:
                parent.active = True
                parent = parent.parent
            active_node = self
        for child in self.children:
            child = child.set_active(href)
            if child:
                active_node = child
        return active_node

    def get_active_items(self):
        if not self.parent:
            return [self]
        else:
            return self.parent.get_active_items() + [self]

    def to_dict(self):
        return {
            'node': self.node,
            'active': self.active,
            'children': [c.to_dict() for c in self.children],
        }


def delete_cache():
    cache.delete('menus')
    for menu in MenuItem.objects.all():
        cache.delete('menu-%s' % menu.slug)
        cache.delete('menu-tree-%s' % menu.slug)


class MenuUnCacheQuerySet(TreeQuerySet):
    def delete(self, *args, **kwargs):
        delete_cache()
        super(MenuUnCacheQuerySet, self).delete(*args, **kwargs)

    def update(self, *args, **kwargs):
        delete_cache()
        super(MenuUnCacheQuerySet, self).update(*args, **kwargs)


MenuItemManager = TreeManager.from_queryset(MenuUnCacheQuerySet)


class MenuItem(MPTTModel):

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    label = models.CharField(
        _('label'),
        max_length=255,
        help_text="The display name on the web site.",
    )
    slug = models.SlugField(
        _('slug'),
        unique=True,
        max_length=255,
        help_text="Unique identifier for this menu item (also CSS ID)"
    )
    order = models.IntegerField(
        _('order'),
        choices=[(x, x) for x in range(0, 51)],
    )
    is_enabled = models.BooleanField(default=True)
    link = models.CharField(
        _('link'),
        max_length=255,
        help_text="The view of the page you want to link to, as a python path or the shortened URL name.",
        blank=True,
    )
    content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
    )
    object_id = models.CharField(
        # use a CharField to be able to point to tables with UUID pks
        max_length=36,
        blank=True,
        db_index=True,
        default=''
    )
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    href = models.CharField(_('href'), editable=False, max_length=255)

    objects = MenuItemManager()

    class Meta:
        ordering = ('lft', 'tree_id')

    class MPTTMeta:
        order_insertion_by = ('order', )

    def to_tree(self):
        cache_key = 'menu-tree-%s' % self.slug
        root = cache.get(cache_key)
        if not root:
            item = root = Item(self)
            descendents = self.get_descendants()
            for prev, curr, next in previous_current_next(descendents):
                previous_item = item
                item = Item(curr)
                if not prev or prev.level < curr.level:
                    previous_item.add_child(item)
                elif prev and prev.level > curr.level:
                    parent = previous_item
                    while parent.node.level >= curr.level:
                        parent = parent.parent
                    parent.add_child(item)
                else:
                    previous_item.parent.add_child(item)
            cache.set(cache_key, root)
        return root

    def save(self, *args, **kwargs):
        literal_url_prefixes = ('/', 'http://', 'https://')
        regex_url_prefixes = ('^',)
        if self.link:
            if any([self.link.startswith(s) for s in literal_url_prefixes]):
                self.href = self.link
            elif any([self.link.startswith(s) for s in regex_url_prefixes]):
                self.href = ''  # regex should not be used as an actual URL
            else:
                self.href = reverse(self.link)
        elif self.content_object:
            self.href = self.content_object.get_absolute_url()
        else:
            self.href = ''
        delete_cache()
        super(MenuItem, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        delete_cache()
        super(MenuItem, self).delete(*args, **kwargs)

    def __unicode__(self):
        return self.slug
