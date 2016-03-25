# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dc_manager', '0006_auto_20160324_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dingcan',
            name='ip_address',
            field=models.IPAddressField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
