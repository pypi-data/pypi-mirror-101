# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['desigz']

package_data = \
{'': ['*'], 'desigz': ['Material/*']}

setup_kwargs = {
    'name': 'desigz',
    'version': '1.0.0',
    'description': 'Modern Graphic Library',
    'long_description': None,
    'author': '6IXK1LL',
    'author_email': 'jxpkaxyz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '==3.9.2',
}


setup(**setup_kwargs)
