# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dc_manager', '0005_auto_20160324_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dingcan',
            name='ip_address',
            field=models.IPAddressField(default=b''),
            preserve_default=True,
        ),
    ]
