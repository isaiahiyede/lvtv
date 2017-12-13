# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchingApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image_obj',
            field=models.ImageField(null=True, upload_to=b'image_obj', blank=True),
        ),
    ]
