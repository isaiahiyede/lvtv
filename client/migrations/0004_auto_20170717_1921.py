# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20170716_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='gethelp',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='providehelp',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
