# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydjantic']

package_data = \
{'': ['*']}

install_requires = \
['dj-database-url>=0.5.0,<0.6.0', 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'pydjantic',
    'version': '0.1.0',
    'description': 'Pydantic Settings for Django',
    'long_description': '# pydjantic\n[![Build Status](https://github.com/ErhoSen/pydjantic/actions/workflows/main.yml/badge.svg)](https://github.com/ErhoSen/pydjantic/actions)\n[![codecov](https://codecov.io/gh/ErhoSen/pydjantic/branch/master/graph/badge.svg?token=BW5A0V3CR3)](https://codecov.io/gh/ErhoSen/pydjantic)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPydantic Settings for Django\n\n___\n### Under Construction\n',
    'author': 'Vladimir Vyazovetskov',
    'author_email': 'erhosen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ErhoSen/pydjantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
