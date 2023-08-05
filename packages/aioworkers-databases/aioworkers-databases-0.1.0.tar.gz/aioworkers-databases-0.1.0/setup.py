# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioworkers_databases']

package_data = \
{'': ['*']}

install_requires = \
['aioworkers>=0.18,<0.19', 'databases>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'aioworkers-databases',
    'version': '0.1.0',
    'description': 'Databases plugin for aioworkers',
    'long_description': "# aioworkers-databases\n\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/aioworkers/aioworkers-databases/CI)](https://github.com/aioworkers/aioworkers-databases/actions?query=workflow%3ACI)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioworkers-databases)](https://pypi.org/project/aioworkers-databases)\n[![PyPI](https://img.shields.io/pypi/v/aioworkers-databases)](https://pypi.org/project/aioworkers-databases)\n\naioworkers plugin for [databases](https://github.com/encode/databases).\n\n## Usage\n\nAdd your database config to aioworkers config:\n\n```yaml\ndb:\n  cls: aioworkers_databases.database.Database\n  dsn: sqlite:///db.sqlite\n```\n\nCreate `Context` for this config and use your db via context:\n\n```python\nawait context.db.execute('CREATE TABLE some_table (id INT);')\n```\n\n## Development\n\nInstall requirements:\n\n```shell\npoetry install\n```\n\nRun tests:\n\n```shell\npytest\n```",
    'author': 'Alexander Bogushov',
    'author_email': 'abogushov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aioworkers/aioworkers-databases',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
