# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['django_parallel_test']
install_requires = \
['Django>=2.2']

setup_kwargs = {
    'name': 'django-parallel-test',
    'version': '0.1.0',
    'description': 'Django test runner to run a test suite across different machines.',
    'long_description': None,
    'author': 'Sid Mitra',
    'author_email': 'django-parallel-test@sidmitra.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
