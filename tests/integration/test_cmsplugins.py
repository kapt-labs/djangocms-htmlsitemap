# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from cms.api import add_plugin
from cms.api import create_page
from cms.models import Placeholder
from django.test.client import RequestFactory
from django.utils.html import strip_spaces_between_tags
import pytest

from djangocms_htmlsitemap import cms_plugins


@pytest.mark.django_db
class TestHtmlSitemapPlugin(object):
    @pytest.fixture(autouse=True)
    def setup_cms(self):
        self.request_factory = RequestFactory()

        # Creates a basic tree of CMS pages
        self.index_page = create_page('Index', 'index.html', 'en', published=True, in_navigation=True)  # noq
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

    def test_can_render_a_simple_tree_of_cms_pages(self):
        # Setup
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            cms_plugins.HtmlSitemapPlugin,
            'fr',
        )

        # Run
        html = model_instance.render_plugin({})
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
            'fr',
            min_depth=2,
        )

        # Run
        html = model_instance.render_plugin({})
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
            'fr',
            max_depth=2,
        )

        # Run
        html = model_instance.render_plugin({})
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
            'fr',
            min_depth=2,
            max_depth=2,
        )

        # Run
        html = model_instance.render_plugin({})
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
            'fr',
            in_navigation=True,
        )

        # Run
        html = model_instance.render_plugin({})
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
            'fr',
            in_navigation=False,
        )

        # Run
        html = model_instance.render_plugin({})
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
