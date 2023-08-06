# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subclean', 'subclean.core', 'subclean.core.section', 'subclean.processors']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['subclean = subclean.cli:main']}

setup_kwargs = {
    'name': 'subclean',
    'version': '0.2.1',
    'description': 'Simple CLI tool to instantly enhance your movie & TV show subtitles.',
    'long_description': '# Subclean\n\n> Simple CLI to instantly enhance your movie & TV show subtitles.\n\n## Installation\n\n```\npip install subclean\n```\n\n## Example\n\n```\n$ subclean subtitle.srt\n12:35:30.337 | INFO | Importing subtitle subtitle.srt\n12:35:30.344 | INFO | BlacklistProcessor running\n12:35:30.397 | INFO | SDHProcessor running\n12:35:30.421 | INFO | DialogProcessor running\n12:35:30.426 | INFO | ErrorProcessor running\n12:35:30.458 | INFO | LineLengthProcessor running\n12:35:30.466 | INFO | Saving subtitle subtitle_clean.srt\n```\n\n![before-after](https://github.com/disrupted/subclean/blob/main/docs/img/subclean-diff.png?raw=true)\n\n## Usage\n\n```\nsubclean [-h] [-v] [-o OUTPUT]\n                   [--processors {LineLength,Dialog,Blacklist,SDH,Error}\n                   [--regex REGEX] [--line-length LINE_LENGTH]\n                   FILE\n\npositional arguments:\n  FILE                  Subtitle file to be processed\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -v, --verbose         Increase output verbosity\n  -o OUTPUT, --output OUTPUT\n                        Set output filename\n  --overwrite           Overwrite input file\n  --processors {LineLength,Dialog,Blacklist,SDH,Error}\n                        Processors to run\n                        (default: Blacklist SDH Dialog Error LineLength)\n  --regex REGEX         Add custom regular expression to BlacklistProcessor\n  --line-length LINE_LENGTH\n                        Maximum total line length when concatenating short lines.\n                        (default: 50)\n```\n',
    'author': 'disrupted',
    'author_email': 'hi@salomonpopp.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/disrupted/subclean',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
