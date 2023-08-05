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
    'version': '0.0.4',
    'description': 'Video Waste Reduction Tool: Automated video editing',
    'long_description': '# Video Waste Reduction Tool in Python\n\n## Intro\n\nThis is a complete python rewrite of [the C++\nvwrt](https://github.com/evnb/vwrt).\n\n## Dependencies\n\n-   python3\n\n-   numpy\n\n-   ffmpeg\n\n## Usage\n\n`user$ vwrt [-i INPUT] [-t SPEED] [-s SPEED] [-o OUTDIR]`\n\n## Required Arguments\n\n-   `-i INPUT` or `--input INPUT`: add input\n    video<sup>[1](#1)</sup>\n\n-   `-t SPEED` or `--talk-speed SPEED`: set talk speed (aka speed when\n    video is above volume threshold)<sup>[1](#1)</sup>\n\n-   `-s SPEED` or `--silence-speed SPEED`: set silence speed (aka speed\n    when video is below volume\n    threshold)<sup>[1](#1)</sup>\n\n-   `-o OUTDIR` or `--outdir OUTDIR`: set output directory\n\n## Optional Arguments\n\n-   `-h` or `--help`: show this help message and exit\n\n-   `-v` or `--verbose`: set verbose mode\n\n-   `-f` or `--add-frames`: overlay timecode on video before processing\n\n-   `-d` or `--dry-run`: skip video processing\n\n1.  Supports multiple arguments of the same type for batch processing. VWRT will cycle\n    through given values until there are no more inputs.\n',
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
