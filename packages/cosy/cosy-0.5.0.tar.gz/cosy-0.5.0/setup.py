# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cosy', 'cosy.skel']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'distro>=1.5.0,<2.0.0',
 'tomlkit>=0.7.0,<0.8.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['cosy = cosy.cli:main']}

setup_kwargs = {
    'name': 'cosy',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'Florian Ludwig',
    'author_email': 'f.ludwig@greyrook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FlorianLudwig/cosy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
