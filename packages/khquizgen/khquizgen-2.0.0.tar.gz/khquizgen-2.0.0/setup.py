# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['khquizgen', 'khquizgen.src']

package_data = \
{'': ['*'], 'khquizgen': ['config/*', 'inputs/*']}

install_requires = \
['dynaconf>=3.1.4,<4.0.0',
 'jellyfish>=0.8.2,<0.9.0',
 'loguru>=0.5.3,<0.6.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.2.3,<2.0.0']

setup_kwargs = {
    'name': 'khquizgen',
    'version': '2.0.0',
    'description': 'Package to randomly autogenerate Kahoot quizzes from notes.',
    'long_description': None,
    'author': 'BGASM',
    'author_email': 'slatte26@msu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
