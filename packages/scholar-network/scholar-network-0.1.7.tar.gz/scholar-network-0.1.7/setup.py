# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scholar_network']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'scholar-network',
    'version': '0.1.7',
    'description': 'Graph Network Analysis for scraping Google Scholar authors.',
    'long_description': '# stuff\n\n# TODO: Add docs using mkdocs and mkdocstrings\n\n# TODO: document functions/classes and module-level as well\n\n# TODO: Fill out README with examples\n',
    'author': 'Nick Anthony',
    'author_email': 'nanthony007@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
