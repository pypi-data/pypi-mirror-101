# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['suggestor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'suggestor',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Alexandre Janvrin',
    'author_email': 'alexandre.janvrin@reseau.eseo.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LivinParadoX/suggestor',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
