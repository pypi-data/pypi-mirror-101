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
    'version': '0.4.0',
    'description': 'Pydantic Settings for Django',
    'long_description': '# pydjantic\n[![Build Status](https://github.com/ErhoSen/pydjantic/actions/workflows/main.yml/badge.svg)](https://github.com/ErhoSen/pydjantic/actions)\n[![codecov](https://codecov.io/gh/ErhoSen/pydjantic/branch/master/graph/badge.svg?token=BW5A0V3CR3)](https://codecov.io/gh/ErhoSen/pydjantic)\n[![pypi](https://img.shields.io/pypi/v/pydjantic.svg)](https://pypi.org/project/pydjantic/)\n[![versions](https://img.shields.io/pypi/pyversions/pydjantic.svg)](https://github.com/ErhoSen/pydjantic)\n[![license](https://img.shields.io/github/license/erhosen/pydjantic.svg)](https://github.com/ErhoSen/pydjantic/blob/master/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**Pydjantic** helps you use Pydantic Settings in your Django applications.\n\n![Pydjantc django settings](https://github.com/ErhoSen/pydjantic/raw/master/images/pydjantic.png "Pydjantc django settings")\n\n## Introduction\n\nIf you are tired of the mess in your Django Settings - I feel your pain:\n* Ridiculously long `settings.py` file, with ASCII-art separators\n* `from common import *` Python [anti-pattern](https://www.geeksforgeeks.org/why-import-star-in-python-is-a-bad-idea/)\n* `try: <import> except: ImportError` Python [anti-pattern](https://stackoverflow.com/questions/14050281/how-to-check-if-a-python-module-exists-without-importing-it)\n* `base.py`, `production.py`, `local.py`, `domain.py` - bunch of unrelated modules that override each other\n* [django-environ](https://github.com/joke2k/django-environ) library, that did even worse...\n\nOn the other hand we have [Pydatic Settings](https://pydantic-docs.helpmanual.io/usage/settings/),\nwhich is de facto standard for all non-django projects.\n\nIf you love Pydatic settings management approach, **Pydjantic** is a right tool for you.\n\n**Pydjantic** allows you to define your settings in familiar way - just inherit from `BaseSettings` like you would in non-django app.\n```py\nfrom typing import List\n\nfrom pydantic import BaseSettings, Field\nfrom pydantic.fields import Undefined\nfrom pydjantic import to_django\n\nclass GeneralSettings(BaseSettings):\n    SECRET_KEY: str = Field(default=Undefined, env=\'DJANGO_SECRET_KEY\')\n    DEBUG: bool = Field(default=False, env=\'DEBUG\')\n    INSTALLED_APPS: List[str] = [\n        \'django.contrib.admin\',\n        \'django.contrib.auth\',\n    ]\n    LANGUAGE_CODE: str = \'en-us\'\n    USE_TZ: bool = True\n\n\nclass StaticSettings(BaseSettings):\n    STATIC_URL: str = \'/static/\'\n    STATIC_ROOT: str = \'staticfiles\'\n\n\nclass SentrySettings(BaseSettings):\n    SENTRY_DSN: str = Field(default=Undefined, env=\'SENTRY_DSN\')\n\n\nclass ProjectSettings(GeneralSettings, StaticSettings, SentrySettings):\n    pass\n\n\nto_django(ProjectSettings())\n```\nYou can create as many classes/modules as you want, to achieve perfect settings\' management.\nDivide your settings by domains, and then create final `ProjectSettings` class, that inherits from these domains.\n\nProvide the instance of `ProjectSettings` to `to_django` function.\nThat\'s all, your django settings will work as expected.\n\n## Installation\n\nInstall using `pip install -U pydjantic` or `poetry add pydjantic`.\n\n## Example\nIn the `/demo` directory you can find a [working Django app](https://github.com/ErhoSen/pydjantic/tree/master/demo) with [pydjantic settings](https://github.com/ErhoSen/pydjantic/blob/master/demo/demo/settings.py).\n\n## Database config\n\n**Pydjantic** comes with a special helper for managing DB configs - `BaseDBConfig`. See example below:\n```py\nfrom pydantic import Field, PostgresDsn\nfrom pydjantic import BaseDBConfig\n\n\nclass DatabaseConfig(BaseDBConfig):\n    default: PostgresDsn = Field(\n        default="postgres://user:password@hostname:5432/database_name", env="DATABASE_URL"\n    )\n\ndb_settings = DatabaseConfig()\nassert db_settings.default == {\n    \'CONN_MAX_AGE\': 0,\n    \'ENGINE\': \'django.db.backends.postgresql_psycopg2\',\n    \'HOST\': \'hostname\',\n    \'NAME\': \'database_name\',\n    \'PASSWORD\': \'password\',\n    \'PORT\': 5432,\n    \'USER\': \'user\',\n}\n```\nTransformation from dsn to django format is done by [dj-database-url](https://pypi.org/project/dj-database-url/).\n',
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
