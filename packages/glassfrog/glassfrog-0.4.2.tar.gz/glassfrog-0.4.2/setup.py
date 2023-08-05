# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glassfrog']

package_data = \
{'': ['*']}

install_requires = \
['requests', 'retrying']

setup_kwargs = {
    'name': 'glassfrog',
    'version': '0.4.2',
    'description': 'Python client for Glassfrog API',
    'long_description': None,
    'author': 'Joao Daher',
    'author_email': 'joao@daher.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
