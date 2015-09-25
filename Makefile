.PHONY: install upgrade coverage travis

install:
		pip install -r dev-requirements.txt
		python setup.py develop

upgrade:
		pip install --upgrade -r dev-requirements.txt
		python setup.py develop --upgrade

coverage:
	py.test --cov-report term-missing --cov djangocms_htmlsitemap

travis: install coverage
