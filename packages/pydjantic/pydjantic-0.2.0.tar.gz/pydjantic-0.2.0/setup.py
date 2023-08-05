# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydjantic']

package_data = \
{'': ['*']}

install_requires = \
['dj-database-url>=0.5.0,<0.6.0', 'pydantic[dotenv]>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'pydjantic',
    'version': '0.2.0',
    'description': 'Pydantic Settings for Django',
    'long_description': '# pydjantic\n[![Build Status](https://github.com/ErhoSen/pydjantic/actions/workflows/main.yml/badge.svg)](https://github.com/ErhoSen/pydjantic/actions)\n[![codecov](https://codecov.io/gh/ErhoSen/pydjantic/branch/master/graph/badge.svg?token=BW5A0V3CR3)](https://codecov.io/gh/ErhoSen/pydjantic)\n[![pypi](https://img.shields.io/pypi/v/pydjantic.svg)](https://pypi.org/project/pydjantic/)\n[![versions](https://img.shields.io/pypi/pyversions/pydjantic.svg)](https://github.com/ErhoSen/pydjantic)\n[![license](https://img.shields.io/github/license/erhosen/pydjantic.svg)](https://github.com/ErhoSen/pydjantic/blob/master/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nUse Pydantic Settings for your Django app.\n\n## Introduction\n\nIf you are tired of the mess in your Django Settings - I feel your pain:\n* Long as Dostoevsky\'s "Crime and punishment" `settings.py` file\n* `from production import *` anti-pattern\n* `try: <import> except: ImportError` anti-pattern\n* `base.py`, `production.py`, `local.py`, `domain.py` - bunch of modules that override each other\n* [django-environ](https://github.com/joke2k/django-environ) library, that did even worse...\n\n**Pydjantic** offers to divide the settings only by their domain:\n```py\nfrom typing import List\n\nfrom pydantic import BaseSettings, Field\nfrom pydantic.fields import Undefined\nfrom pydjantic import to_django\n\nclass GeneralSettings(BaseSettings):\n    SECRET_KEY: str = Field(default=Undefined, env=\'DJANGO_SECRET_KEY\')\n    DEBUG: bool = Field(default=False, env=\'DEBUG\')\n    INSTALLED_APPS: List[str] = [\n        \'django.contrib.admin\',\n        \'django.contrib.auth\',\n    ]\n    LANGUAGE_CODE: str = \'en-us\'\n    USE_TZ: bool = True\n\n\nclass StaticSettings(BaseSettings):\n    STATIC_URL: str = \'/static/\'\n    STATIC_ROOT: str = \'staticfiles\'\n\n\nclass SentrySettings(BaseSettings):\n    SENTRY_DSN: str = Field(default=Undefined, env=\'SENTRY_DSN\')\n\n\nclass ProjectSettings(GeneralSettings, StaticSettings, SentrySettings):\n    pass\n\n\nto_django(ProjectSettings())\n```\nYou can create as many classes/modules as you want, to achieve perfect settings management.\n\nJust create final `ProjectSettings` class, that inherits from these domains, and provide its instance to `to_django` function.\nThat\'s all, your django settings will work as expected.\n\n## Installation\n\nInstall using `pip install -U pydantic` or `poetry add pydjantic`.\n',
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
