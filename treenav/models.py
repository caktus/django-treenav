from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import mptt


class MenuItem(models.Model):
    ORDER_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
    )
    
    parent = models.ForeignKey(
        'MenuItem',
        related_name='children',
        null=True,
        blank=True,
    )
    label = models.CharField(
        _('label'),
        max_length=255,
        help_text="The display name on the web site.",
    )
    slug = models.CharField(
        _('slug'),
        unique=True,
        max_length=255,
        help_text="Unique identifier for this menu item (also CSS ID)"
    )
    order = models.IntegerField(
        _('order'),
        choices=ORDER_CHOICES,
    )
    is_enabled = models.BooleanField(default=True)
    link = models.CharField(
        _('link'),
        max_length=255,
        help_text="The view of the page you want to link to, as a python path or the shortened URL name.",
        null=True,
        blank=True,
    )
    content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    href = models.CharField(_('href'), editable=False, max_length=255)
    
    
    def height(self):
        """ Returns height of node in tree """
        if self.parent:
            return self.parent.height() + 1
        else:
            return 1
    
    def up(self):
        if self.parent:
            return self.parent
        else:
            return self.menu
    
    def __unicode__(self):
        return self.slug

mptt.register(MenuItem, order_insertion_by=['order'])