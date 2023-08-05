# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kak_plugins', 'kak_plugins.apis']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.14,<4.0.0']

entry_points = \
{'console_scripts': ['github-permalink = kak_plugins.github_permalink:main']}

setup_kwargs = {
    'name': 'kak-plugins',
    'version': '0.3.1',
    'description': '',
    'long_description': '[![Tests](https://github.com/abstractlyZach/kak_plugins/workflows/Tests/badge.svg)](https://github.com/abstractlyZach/kak_plugins/actions?workflow=Tests)\n[![PyPI](https://img.shields.io/pypi/v/kak-plugins.svg)](https://pypi.org/project/kak-plugins/)\n[![Codecov](https://codecov.io/gh/abstractlyZach/kak_plugins/branch/main/graph/badge.svg)](https://codecov.io/gh/abstractlyZach/kak_plugins)\n\n\n# kak_plugins\n',
    'author': 'abstractlyZach',
    'author_email': 'zach3lee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abstractlyZach/kak_plugins',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
