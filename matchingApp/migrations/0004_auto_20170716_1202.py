# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchingApp', '0003_auto_20170716_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchparticipants',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
