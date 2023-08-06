# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hltb_oracle']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'hltb-oracle',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Matteo Silvestro',
    'author_email': 'matteosilvestro@live.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
