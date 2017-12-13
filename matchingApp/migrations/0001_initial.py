# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('support_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='MatchParticipants',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_paired', models.CharField(max_length=150, null=True, blank=True)),
                ('confirmation_image', models.ImageField(null=True, upload_to=b'confirmation', blank=True)),
                ('paired', models.BooleanField(default=False)),
                ('confirmed', models.BooleanField(default=False)),
                ('payment_made', models.BooleanField(default=False)),
                ('payment_received', models.BooleanField(default=False)),
                ('amt_matched', models.FloatField(default=0, max_length=50)),
                ('deleted', models.BooleanField(default=False)),
                ('track_order', models.CharField(max_length=30, null=True, blank=True)),
                ('gethelp', models.ForeignKey(blank=True, to='client.GetHelp', null=True)),
                ('giver', models.ForeignKey(related_name='Giver', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('providehelp', models.ForeignKey(blank=True, to='client.ProvideHelp', null=True)),
                ('receiver', models.ForeignKey(related_name='Receiver', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Matched Participants',
            },
        ),
        migrations.CreateModel(
            name='MessageCenterComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.TextField()),
                ('no_of_comments', models.IntegerField(default=0)),
                ('new', models.BooleanField(default=True)),
                ('replied', models.BooleanField(default=False)),
                ('resolved', models.BooleanField(default=False)),
                ('replied_on', models.DateTimeField(null=True)),
                ('archive', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('admin', models.BooleanField(default=False)),
                ('subject', models.CharField(max_length=150, null=True, blank=True)),
                ('image_obj', models.ImageField(null=True, upload_to=b'image_obj', blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('gethelp', models.ForeignKey(blank=True, to='client.GetHelp', null=True)),
                ('matches', models.OneToOneField(null=True, blank=True, to='matchingApp.MatchParticipants')),
                ('providehelp', models.ForeignKey(blank=True, to='client.ProvideHelp', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='message_obj',
            field=models.ForeignKey(blank=True, to='matchingApp.MessageCenterComment', null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
