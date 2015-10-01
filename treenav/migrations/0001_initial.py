# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(help_text=b'The display name on the web site.', max_length=255, verbose_name='label')),
                ('slug', models.SlugField(help_text=b'Unique identifier for this menu item (also CSS ID)', unique=True, max_length=255, verbose_name='slug')),
                ('order', models.IntegerField(verbose_name='order', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50)])),
                ('is_enabled', models.BooleanField(default=True)),
                ('link', models.CharField(help_text=b'The view of the page you want to link to, as a python path or the shortened URL name.', max_length=255, verbose_name='link', blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('href', models.CharField(verbose_name='href', max_length=255, editable=False)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='treenav.MenuItem', null=True)),
            ],
            options={
                'ordering': ('lft', 'tree_id'),
            },
        ),
    ]
