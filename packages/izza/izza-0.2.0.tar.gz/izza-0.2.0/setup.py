# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['izza',
 'izza.exploration',
 'izza.modeling',
 'izza.modeling.feature_eng',
 'izza.validation']

package_data = \
{'': ['*']}

install_requires = \
['MiniSom>=2.2.8,<3.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'pandas>=1.2.3,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0']

setup_kwargs = {
    'name': 'izza',
    'version': '0.2.0',
    'description': 'my machine learning toolkit',
    'long_description': None,
    'author': 'Ismael Lachheb',
    'author_email': 'ismael.lachheb@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
