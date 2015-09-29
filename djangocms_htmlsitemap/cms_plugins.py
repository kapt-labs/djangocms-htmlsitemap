# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pagemodel import Page
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from .models import HtmlSitemapPluginConf


class HtmlSitemapPlugin(CMSPluginBase):
    model = HtmlSitemapPluginConf
    name = _('HTML Sitemap')

    render_template = 'djangocms_htmlsitemap/sitemap.html'

    def render(self, context, instance, placeholder):
        site = Site.objects.get_current()
        pages = Page.objects.public().published(site=site).order_by('path') \
            .filter(depth__gte=instance.min_depth).distinct()
        if instance.max_depth:
            pages = pages.filter(depth__lte=instance.max_depth)
        if instance.in_navigation is not None:
            pages = pages.filter(in_navigation=instance.in_navigation)

        context['instance'] = instance
        context['pages'] = pages
        context['annotated_pages'] = Page.get_annotated_list_qs(pages)

        return context


plugin_pool.register_plugin(HtmlSitemapPlugin)
