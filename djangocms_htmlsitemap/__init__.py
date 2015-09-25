# -*- coding: utf-8 -*-

pkg_resources = __import__('pkg_resources')
distribution = pkg_resources.get_distribution('djangocms-htmlsitemap')
__version__ = distribution.version
