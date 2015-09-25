# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20150419_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='HtmlSitemapPluginConf',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('min_depth', models.PositiveIntegerField(default=0, verbose_name='Minimum depth')),
                ('max_depth', models.PositiveIntegerField(null=True, verbose_name='Maximum depth', blank=True)),
                ('in_navigation', models.NullBooleanField(default=None, verbose_name='In navigation')),
            ],
            options={
                'verbose_name': 'HTML Sitemap plugin configuration',
                'verbose_name_plural': 'HTML Sitemap plugin configurations',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
