# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GetHelp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('package', models.CharField(blank=True, max_length=250, null=True, choices=[(b'', b'Select Package'), (b'50000', b'50000'), (b'100000', b'100000'), (b'200000', b'200000'), (b'500000', b'500000'), (b'1000000', b'1000000')])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('edited_on', models.DateTimeField(auto_now_add=True)),
                ('deleted_on', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('message_text', models.CharField(max_length=350, null=True, blank=True)),
                ('amount', models.CharField(max_length=150, null=True, blank=True)),
                ('tracking_number', models.CharField(max_length=30, null=True, blank=True)),
                ('tAndC', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'New', max_length=50)),
                ('help_requested', models.BooleanField(default=False)),
                ('rel_to', models.CharField(max_length=50, null=True, blank=True)),
                ('amount_requested', models.CharField(max_length=150, null=True, blank=True)),
                ('paired', models.BooleanField(default=False)),
                ('amt_paired', models.FloatField(default=0, max_length=50)),
                ('amt_left', models.FloatField(default=0, max_length=50)),
                ('paired_rel_to', models.BooleanField(default=False)),
                ('testimony', models.BooleanField(default=False)),
                ('getHelp', models.BooleanField(default=False)),
                ('user_account', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name_plural': 'Get Help',
            },
        ),
        migrations.CreateModel(
            name='ProvideHelp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('package', models.CharField(blank=True, max_length=250, null=True, choices=[(b'', b'Select Package'), (b'50000', b'50000'), (b'100000', b'100000'), (b'200000', b'200000'), (b'500000', b'500000'), (b'1000000', b'1000000')])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('edited_on', models.DateTimeField(auto_now_add=True)),
                ('deleted_on', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('message_text', models.CharField(max_length=350, null=True, blank=True)),
                ('amount', models.CharField(max_length=150, null=True, blank=True)),
                ('tracking_number', models.CharField(max_length=30, null=True, blank=True)),
                ('tAndC', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'New', max_length=50)),
                ('help_requested', models.BooleanField(default=False)),
                ('rel_to', models.CharField(max_length=50, null=True, blank=True)),
                ('amount_requested', models.CharField(max_length=150, null=True, blank=True)),
                ('paired', models.BooleanField(default=False)),
                ('amt_paired', models.FloatField(default=0, max_length=50)),
                ('amt_left', models.FloatField(default=0, max_length=50)),
                ('paired_rel_to', models.BooleanField(default=False)),
                ('testimony', models.BooleanField(default=False)),
                ('provideHelp', models.BooleanField(default=False)),
                ('user_account', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name_plural': 'Provide Help',
            },
        ),
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=500, null=True, blank=True)),
                ('testimony_image', models.FileField(null=True, upload_to=b'confirmation', blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('default_text', models.CharField(max_length=350, null=True, blank=True)),
                ('testimony_gh', models.ForeignKey(blank=True, to='client.GetHelp', null=True)),
                ('testimony_ph', models.ForeignKey(blank=True, to='client.ProvideHelp', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Testimonials',
            },
        ),
    ]
