# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testfinder']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'testfinder',
    'version': '0.0.1',
    'description': 'Find test cases on a Python project.',
    'long_description': '# testfinder',
    'author': 'Sid Mitra',
    'author_email': 'testfinder@sidmitra.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
