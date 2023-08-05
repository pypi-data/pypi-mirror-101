# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flixpy',
 'flixpy.browse',
 'flixpy.enums',
 'flixpy.models',
 'flixpy.models.show']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'flixpy',
    'version': '0.0.3.post1',
    'description': '',
    'long_description': None,
    'author': 'ninest',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
