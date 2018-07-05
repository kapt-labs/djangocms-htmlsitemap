# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import pytest

from cms import __version__
from cms.api import add_plugin
from cms.api import create_page
from cms.api import create_title
from cms.api import publish_page
from cms.models import Placeholder
from django.conf import settings
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.utils.html import strip_spaces_between_tags
from django.utils.translation import activate
from django.template import RequestContext

from djangocms_htmlsitemap import cms_plugins


def get_cms_version():
    return tuple(map(lambda i: int(i), __version__.split('.')))


if get_cms_version() >= (3, 4):
    from cms.plugin_rendering import ContentRenderer


@pytest.mark.django_db
class TestHtmlSitemapPlugin(object):
    @pytest.fixture(autouse=True)
    def setup_cms(self):
        # Creates a request
        self.request = self.get_request()

        # Creates a test user
        self.user = User.objects.create(username='testuser', is_active=True, is_superuser=True)

        # Creates a basic tree of CMS pages
        self.index_page = create_page('Index', 'index.html', 'en', published=True, in_navigation=True)  # noq

        try:
            # django-cms 3.5+
            self.index_page.set_as_homepage()
        except AttributeError:
            # django-cms < 3.5 defaults the first page as being the home page
            pass

        self.depth2_page1 = create_page(
            'Depth 2 page 1', 'simple.html', 'en', in_navigation=True, published=True, parent=self.index_page)
        self.depth2_page2 = create_page(
            'Depth 2 page 2', 'simple.html', 'en', in_navigation=False, published=True, parent=self.index_page)
        self.depth3_page1 = create_page(
            'Depth 3 page 1', 'simple.html', 'en', in_navigation=False, published=True, parent=self.depth2_page2)
        self.depth3_page2 = create_page(
            'Depth 3 page 2', 'simple.html', 'en', in_navigation=False, published=True, parent=self.depth2_page2)
        self.depth2_page3 = create_page(
            'Depth 2 page 3', 'simple.html', 'en', in_navigation=False, published=True, parent=self.index_page)
        self.depth2_page4 = create_page(
            'Depth 2 page 4', 'simple.html', 'en', in_navigation=False, published=True, parent=self.index_page)
        self.depth3_page3 = create_page(
            'Depth 3 page 3', 'simple.html', 'en', in_navigation=False, published=True, parent=self.depth2_page4)

    def get_request(self):
        factory = RequestFactory()

        if settings.USE_I18N:
            language = settings.LANGUAGES[0][0]
        else:
            language = settings.LANGUAGE_CODE

        request = factory.get('/')
        request.LANGUAGE_CODE = language
        request.current_page = None
        return request

    def render_plugin(self, instance):
        context = RequestContext(self.request, {'request': self.request})

        if get_cms_version() >= (3, 4):
            renderer = ContentRenderer(request=self.request)
            return renderer.render_plugin(instance, context)
        else:
            return instance.render_plugin(context)

    def test_can_render_a_simple_tree_of_cms_pages(self):
        # Setup
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            cms_plugins.HtmlSitemapPlugin,
            'en',
        )

        # Run
        html = self.render_plugin(model_instance)
        html = strip_spaces_between_tags(html)

        # Check
        assert html.strip() == strip_spaces_between_tags(
            """
                <div id="sitemap">
                    <ul>
                        <li>
                            <a href="/" title="Index">Index</a>
                            <ul>
                                <li><a href="/depth-2-page-1/" title="Depth 2 page 1">Depth 2 page 1</a></li>
                                <li>
                                    <a href="/depth-2-page-2/" title="Depth 2 page 2">Depth 2 page 2</a>
                                    <ul>
                                        <li><a href="/depth-2-page-2/depth-3-page-1/" title="Depth 3 page 1">Depth 3 page 1</a></li>
                                        <li><a href="/depth-2-page-2/depth-3-page-2/" title="Depth 3 page 2">Depth 3 page 2</a></li>
                                    </ul>
                                </li>
                                <li><a href="/depth-2-page-3/" title="Depth 2 page 3">Depth 2 page 3</a></li>
                                <li>
                                    <a href="/depth-2-page-4/" title="Depth 2 page 4">Depth 2 page 4</a>
                                    <ul>
                                        <li><a href="/depth-2-page-4/depth-3-page-3/" title="Depth 3 page 3">Depth 3 page 3</a></li>
                                    </ul>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </div>
            """).strip()

    def test_can_render_a_simple_tree_of_cms_pages_from_a_minimum_depth(self):
        # Setup
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            cms_plugins.HtmlSitemapPlugin,
            'en',
            min_depth=2,
        )

        # Run
        html = self.render_plugin(model_instance)
        html = strip_spaces_between_tags(html)

        # Check
        assert html.strip() == strip_spaces_between_tags(
            """
                <div id="sitemap">
                    <ul>
                        <li><a href="/depth-2-page-1/" title="Depth 2 page 1">Depth 2 page 1</a></li>
                        <li>
                            <a href="/depth-2-page-2/" title="Depth 2 page 2">Depth 2 page 2</a>
                            <ul>
                                <li><a href="/depth-2-page-2/depth-3-page-1/" title="Depth 3 page 1">Depth 3 page 1</a></li>
                                <li><a href="/depth-2-page-2/depth-3-page-2/" title="Depth 3 page 2">Depth 3 page 2</a></li>
                            </ul>
                        </li>
                        <li><a href="/depth-2-page-3/" title="Depth 2 page 3">Depth 2 page 3</a></li>
                        <li>
                            <a href="/depth-2-page-4/" title="Depth 2 page 4">Depth 2 page 4</a>
                            <ul>
                                <li><a href="/depth-2-page-4/depth-3-page-3/" title="Depth 3 page 3">Depth 3 page 3</a></li>
                            </ul>
                        </li>
                    </ul>
                </div>
            """).strip()

    def test_can_render_a_simple_tree_of_cms_pages_to_a_maximum_depth(self):
        # Setup
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            cms_plugins.HtmlSitemapPlugin,
            'en',
            max_depth=2,
        )

        # Run
        html = self.render_plugin(model_instance)
        html = strip_spaces_between_tags(html)

        # Check
        assert html.strip() == strip_spaces_between_tags(
            """
                <div id="sitemap">
                    <ul>
                        <li>
                            <a href="/" title="Index">Index</a>
                            <ul>
                                <li><a href="/depth-2-page-1/" title="Depth 2 page 1">Depth 2 page 1</a></li>
                                <li>
                                    <a href="/depth-2-page-2/" title="Depth 2 page 2">Depth 2 page 2</a>
                                </li>
                                <li><a href="/depth-2-page-3/" title="Depth 2 page 3">Depth 2 page 3</a></li>
                                <li>
                                    <a href="/depth-2-page-4/" title="Depth 2 page 4">Depth 2 page 4</a>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </div>
            """).strip()

    def test_can_render_a_simple_tree_of_cms_pages_from_a_minimum_depth_to_a_maximum_depth(self):
        # Setup
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            cms_plugins.HtmlSitemapPlugin,
            'en',
            min_depth=2,
            max_depth=2,
        )

        # Run
        html = self.render_plugin(model_instance)
        html = strip_spaces_between_tags(html)

        # Check
        assert html.strip() == strip_spaces_between_tags(
            """
                <div id="sitemap">
                    <ul>
                        <li><a href="/depth-2-page-1/" title="Depth 2 page 1">Depth 2 page 1</a></li>
                        <li>
                            <a href="/depth-2-page-2/" title="Depth 2 page 2">Depth 2 page 2</a>
                        </li>
                        <li><a href="/depth-2-page-3/" title="Depth 2 page 3">Depth 2 page 3</a></li>
                        <li>
                            <a href="/depth-2-page-4/" title="Depth 2 page 4">Depth 2 page 4</a>
                        </li>
                    </ul>
                </div>
            """).strip()

    def test_can_render_a_simple_tree_of_cms_pages_that_are_in_navigation(self):
        # Setup
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            cms_plugins.HtmlSitemapPlugin,
            'en',
            in_navigation=True,
        )

        # Run
        html = self.render_plugin(model_instance)
        html = strip_spaces_between_tags(html)

        # Check
        assert html.strip() == strip_spaces_between_tags(
            """
                <div id="sitemap">
                    <ul>
                        <li>
                            <a href="/" title="Index">Index</a>
                            <ul>
                                <li><a href="/depth-2-page-1/" title="Depth 2 page 1">Depth 2 page 1</a></li>
                            </ul>
                        </li>
                    </ul>
                </div>
            """).strip()

    def test_can_render_a_simple_tree_of_cms_pages_that_are_not_in_navigation(self):
        # Setup
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            cms_plugins.HtmlSitemapPlugin,
            'en',
            in_navigation=False,
        )

        # Run
        html = self.render_plugin(model_instance)
        html = strip_spaces_between_tags(html)

        # Check
        assert html.strip() == strip_spaces_between_tags(
            """
                <div id="sitemap">
                    <ul>
                        <li>
                            <a href="/depth-2-page-2/" title="Depth 2 page 2">Depth 2 page 2</a>
                            <ul>
                                <li><a href="/depth-2-page-2/depth-3-page-1/" title="Depth 3 page 1">Depth 3 page 1</a></li>
                                <li><a href="/depth-2-page-2/depth-3-page-2/" title="Depth 3 page 2">Depth 3 page 2</a></li>
                            </ul>
                        </li>
                        <li><a href="/depth-2-page-3/" title="Depth 2 page 3">Depth 2 page 3</a></li>
                        <li>
                            <a href="/depth-2-page-4/" title="Depth 2 page 4">Depth 2 page 4</a>
                            <ul>
                                <li><a href="/depth-2-page-4/depth-3-page-3/" title="Depth 3 page 3">Depth 3 page 3</a></li>
                            </ul>
                        </li>
                    </ul>
                </div>
            """).strip()

    def test_can_render_sitemap_in_other_language(self):
        create_title(
            'fr', 'Index fr', self.index_page)

        create_title(
            'fr', 'Niveau 2 Page 1', self.depth2_page1)

        publish_page(self.index_page, self.user, 'fr')
        publish_page(self.depth2_page1, self.user, 'fr')

        activate('fr')
        self.request.LANGUAGE_CODE = 'fr'

        # Setup
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            cms_plugins.HtmlSitemapPlugin,
            'fr',
            in_navigation=True,
        )

        # Run
        html = self.render_plugin(model_instance)
        html = strip_spaces_between_tags(html)

        # Check
        assert html.strip() == strip_spaces_between_tags(
            """
                <div id="sitemap">
                    <ul>
                        <li>
                            <a href="/" title="Index fr">Index fr</a>
                            <ul>
                                <li>
                                    <a href="/niveau-2-page-1/" title="Niveau 2 Page 1">Niveau 2 Page 1</a>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </div>
            """).strip()
