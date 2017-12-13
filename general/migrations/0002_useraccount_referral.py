# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='referral',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
