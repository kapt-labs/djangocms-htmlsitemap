from os.path import abspath, dirname, join

from setuptools import find_packages, setup


def read_relative_file(filename):
    """
    Returns contents of the given file, whose path is supposed relative
    to this module.
    """
    with open(join(dirname(abspath(__file__)), filename)) as f:
        return f.read()


setup(
    name="djangocms-htmlsitemap",
    version="0.5.0",
    author="Kapt",
    author_email="dev@kapt.mobi",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/kapt-labs/djangocms-htmlsitemap",
    license="BSD",
    description="A Django CMS plugin for building HTML sitemaps showing organized lists of CMS pages.",
    long_description=read_relative_file("README.rst"),
    zip_safe=False,
    install_requires=["django>=1.11", "django-cms>=3.1"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
