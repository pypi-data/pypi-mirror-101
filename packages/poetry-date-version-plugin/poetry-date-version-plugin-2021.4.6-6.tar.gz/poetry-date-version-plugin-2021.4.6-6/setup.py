# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_date_version_plugin']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=1.0.0a1,<1.0.0', 'poetry>=1.2.0a0']

entry_points = \
{'poetry.application.plugin': ['plugin = '
                               'poetry_date_version_plugin.plugin:VersionPlugin']}

setup_kwargs = {
    'name': 'poetry-date-version-plugin',
    'version': '2021.4.6-6',
    'description': '',
    'long_description': 'None',
    'author': 'Dustyn Gibson',
    'author_email': 'miigotu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
