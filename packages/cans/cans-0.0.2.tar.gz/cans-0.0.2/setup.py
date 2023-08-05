# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cans']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 'docs': ['sphinx>=3.5.3,<4.0.0']}

setup_kwargs = {
    'name': 'cans',
    'version': '0.0.2',
    'description': 'Robust, composable, functional containers',
    'long_description': '🥫 Cans\n=======\n\n.. image:: https://img.shields.io/pypi/v/cans.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/cans\n\n.. image:: https://img.shields.io/pypi/l/cans.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/cans\n\n.. image:: https://img.shields.io/pypi/pyversions/cans.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/cans\n\n.. image:: https://img.shields.io/readthedocs/cans.svg?style=flat-square\n   :target: http://cans.readthedocs.io/\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square\n   :target: https://github.com/psf/black\n\nComposable, robust, functional containers like ``Maybe``.\nProperly typed and supports pattern matching on Python 3.10+.\n\nQuickstart\n----------\n\n.. code-block:: python3\n\n   >>> from cans import Just, Nothing\n   >>> greeting = Just("hello")\n   >>> greeting.map(str.upper)\n   Just("HELLO")\n   ...\n   >>> # Python 3.10+ only\n   >>> match greeting:\n   ...     case Just(n):\n   ...         print(f"{greeting.title()} world!")\n   ...     case Nothing():\n   ...         print("Hi world!")\n   Hello world!\n\nAmong the supported methods are ``flatmap``, ``filter``, ``zip``,\nas well as the relevant\n`collection APIs <https://docs.python.org/3/library/collections.abc.html>`_.\n\nTodo\n----\n\n- Other containers\n',
    'author': 'Arie Bovenberg',
    'author_email': 'a.c.bovenberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ariebovenberg/cans',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
