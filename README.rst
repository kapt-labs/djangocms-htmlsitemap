=====================
djangocms-htmlsitemap
=====================

.. image:: http://img.shields.io/travis/kapt-labs/djangocms-htmlsitemap.svg?style=flat-square
    :target: http://travis-ci.org/kapt-labs/djangocms-htmlsitemap
    :alt: Build status

.. image:: http://img.shields.io/coveralls/kapt-labs/djangocms-htmlsitemap.svg?style=flat-square
    :target: https://coveralls.io/r/kapt-labs/djangocms-htmlsitemap
    :alt: Coveralls status

*A Django CMS plugin for building HTML sitemaps showing organized lists of CMS pages.*

.. contents:: :local:

Installation
-------------

Just run:

::

  pip install djangocms-htmlsitemap

Once installed you just need to add ``djangocms_htmlsitemap`` to ``INSTALLED_APPS`` in your project's settings module:

::

  INSTALLED_APPS = (
      # other apps
      'djangocms_htmlsitemap',
  )

Then install the models:

::

  python manage.py syncdb

If you are using Django 1.6, you should use South 1.0 in order to benefit from the migrations. This way you can use the migration command provided by South:

::

  python manage.py migrate djangocms_htmlsitemap

*Congrats! You’re in.*

Authors
-------

Kapt and Contributors <dev@kapt.mobi>

License
-------

BSD. See ``LICENSE`` for more details.
