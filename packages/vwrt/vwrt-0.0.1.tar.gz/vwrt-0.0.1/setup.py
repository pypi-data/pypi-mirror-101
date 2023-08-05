# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vwrt']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.2,<1.20.0']

entry_points = \
{'console_scripts': ['vwrt = vwrt.vwrt:main']}

setup_kwargs = {
    'name': 'vwrt',
    'version': '0.0.1',
    'description': 'Video Waste Reduction Tool: Automated video editing',
    'long_description': None,
    'author': 'Evan Binder',
    'author_email': 'evanmbinder@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/evnb/vwrt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
