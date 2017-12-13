# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_auto_20170629_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='defaulter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='defaulter_msg',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
