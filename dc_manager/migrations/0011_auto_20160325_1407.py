# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dc_manager', '0010_auto_20160325_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dingcan',
            name='ip_address',
            field=models.CharField(max_length=30),
            preserve_default=True,
        ),
    ]
