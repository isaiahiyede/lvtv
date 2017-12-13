# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('matchingApp', '0002_comment_image_obj'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matchparticipants',
            options={'ordering': ['-created_on'], 'verbose_name_plural': 'Matched Participants'},
        ),
        migrations.AddField(
            model_name='matchparticipants',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
