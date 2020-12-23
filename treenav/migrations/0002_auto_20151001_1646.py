# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("treenav", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menuitem",
            name="object_id",
            field=models.CharField(
                default="", max_length=36, db_index=True, blank=True
            ),
        ),
    ]
