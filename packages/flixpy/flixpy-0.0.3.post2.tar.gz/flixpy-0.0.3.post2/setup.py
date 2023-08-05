# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flixpy',
 'flixpy.browse',
 'flixpy.enums',
 'flixpy.models',
 'flixpy.models.show']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'flixpy',
    'version': '0.0.3.post2',
    'description': '',
    'long_description': '<h1 align="center">\n  <img src="assets/logo.svg" width=95>\n  <br>\n  Flixpy\n</h1>\n\n<p align="center">\nInformation on movies, shows, streaming platforms, people, and more\n</p>\n\n<!-- Badges -->\n<p align="center">\n  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/ninest/flixpy/PyTest?style=flat-square">\n  <a href="https://pypi.org/project/flixpy/">\n    <img src="https://img.shields.io/pypi/v/flixpy?color=blue&style=flat-square" alt="Version" />\n  </a>\n  <a href="https://pypi.org/project/flixpy/">\n    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/flixpy?color=red&style=flat-square" />\n  </a>\n\n  <img src="https://img.shields.io/github/license/ninest/flixpy?style=flat-square" alt="MIT" />\n  <a href="https://www.buymeacoffee.com/ninest">\n    <img src="https://img.shields.io/badge/Donate-Buy%20Me%20A%20Coffee-orange.svg?style=flat-square" alt="Buy Me A Coffee">\n  </a>\n</p>\n\n## Links\n\n- [Documentation](http://flixpy.now.sh/)\n- [Examples](https://github.com/ninest/flixpy/tree/master/examples)\n- [Discussions](https://github.com/ninest/flixpy/discussions)\n\n## Features\n\n- [x] Movies and TV shows\n  - [x] Get streaming providers and a direct link to watch\n  - [x] Get the direct link to watch each episode\n  - [x] View metadata such as title, overview, ratings, actors\n- [ ] Searching and browsing\n  - [ ] Search filters (sort by rating, tag, genre)\n- [ ] Actors\n\n### Experimental\n\n- [ ] Integration with Popcorn API\n- [ ] Functions to download subtitles for movies and episodes\n\n## Usage\n\n### Installation\n\n```bash\npip3 install flixpy\n```\n\n### Basic examples\n\n**Get the a movie\'s Netflix link:**\n\n```py\nfrom flixpy import Movie, StreamingProvider\n\nmovie = Movie("extraction-2020")\n\nif movie.is_on(StreamingProvider.NETFLIX):\n  netflix_link = movie.link_for(StreamingProvider.NETFLIX)\n  # => https://www.netflix.com/watch/80230399\n```\n\n**List all episodes in a show:**\n\n```py\nfrom flixpy import Show\n\nshow = Show("breaking-bad-2008")\n\nfor season in show:\n  for episode in season:\n    print(episode.title)\n```\n\n**List genres of a show:**\n\n```py\nfrom flixpy import Show\n\nshow = Show(\'breaking-bad-2008\')\nshow.genres\n# => [<Genre.CRIME>, <Genre.THRILLER>]\n```\n\n**Browse animated shows in Amazon Prime Video:**\n\n```\nComing soon\n```\n\nSee more examples in the [documentation](http://flixpy.now.sh/).\n\n### Contributing\n\nFlixpy uses [`poetry`](https://python-poetry.org/). To set up your environment, clone or download this repository then run the following commands:\n\n```bash\npoetry install\npoetry shell\n```\n\n## License\n\nMIT\n',
    'author': 'ninest',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ninest/armorstand/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
