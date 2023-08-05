# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_simple_timeseries']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-simple-timeseries',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mike wakerly',
    'author_email': 'opensource@hoho.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
