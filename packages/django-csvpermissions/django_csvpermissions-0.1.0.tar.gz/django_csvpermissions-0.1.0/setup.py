# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv_permissions']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2', 'isort>=4']

setup_kwargs = {
    'name': 'django-csvpermissions',
    'version': '0.1.0',
    'description': 'CSV Based Permissions Module for Django',
    'long_description': '# CSV Permissions Module for Django\n\n<Insert Readme Here>\n\n',
    'author': 'Alliance Software',
    'author_email': 'support@alliancesoftware.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
