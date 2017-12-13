# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0006_auto_20170717_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='defaulter_msg',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
