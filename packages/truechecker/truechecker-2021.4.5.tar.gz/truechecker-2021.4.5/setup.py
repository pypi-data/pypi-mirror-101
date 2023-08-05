# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['truechecker', 'truechecker.models', 'truechecker.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<3.8', 'certifi>=2020.12.5,<2021.0.0', 'pydantic>=1.8.1,<2.0.0']

extras_require = \
{':sys_platform == "darwin"': ['ujson>=4.0,<4.1', 'uvloop>=0.15,<0.16'],
 ':sys_platform == "linux"': ['ujson>=4.0,<4.1',
                              'uvloop>=0.15,<0.16',
                              'ciso8601>=2.1,<2.2']}

setup_kwargs = {
    'name': 'truechecker',
    'version': '2021.4.5',
    'description': 'Python client for True Checker API',
    'long_description': '# True Checker Python\n\nPython client library for True Checker API',
    'author': 'Oleg A.',
    'author_email': 'oleg@trueweb.app',
    'maintainer': 'Oleg A.',
    'maintainer_email': 'oleg@trueweb.app',
    'url': 'https://gitlab.com/true-web-app/true-checker/true-checker-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
