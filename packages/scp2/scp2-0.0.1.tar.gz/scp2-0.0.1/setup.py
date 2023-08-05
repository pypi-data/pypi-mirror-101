# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scp2']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'more-itertools>=8.7.0,<9.0.0',
 'paramiko>=2.7.2,<3.0.0']

entry_points = \
{'console_scripts': ['scp2 = scp2.core:scp2']}

setup_kwargs = {
    'name': 'scp2',
    'version': '0.0.1',
    'description': 'scp real over ssh',
    'long_description': None,
    'author': 'alingse',
    'author_email': 'alingse@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
