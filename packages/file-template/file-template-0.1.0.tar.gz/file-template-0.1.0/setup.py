# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_template']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'file-template',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alexandre Janvrin',
    'author_email': 'alexandre.janvrin@reseau.eseo.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
