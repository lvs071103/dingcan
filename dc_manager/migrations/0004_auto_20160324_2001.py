# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dc_manager', '0003_dingcan_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dingcan',
            name='ip_address',
            field=models.IPAddressField(blank=True),
            preserve_default=True,
        ),
    ]
