# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pnpm']

package_data = \
{'': ['*'],
 'pnpm': ['generator/__pkg__/*',
          'generator/__pkg__/.pnpm/scripts/*',
          'generator/__pkg__/docs/*',
          'generator/__pkg__/src/*',
          'generator/__pkg__/src/.build_assets/*',
          'generator/__pkg__/src/icons/*',
          'generator/__pkg__/src/styles/*',
          'generator/__pkg__/test/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'numpy>=1.20.1,<2.0.0',
 'rglob>=1.7,<2.0',
 'rich>=9.13.0,<10.0.0']

setup_kwargs = {
    'name': 'pnpm',
    'version': '0.2.38',
    'description': '',
    'long_description': None,
    'author': 'robo-monk',
    'author_email': 'rrobomonk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.1,<4.0',
}


setup(**setup_kwargs)
