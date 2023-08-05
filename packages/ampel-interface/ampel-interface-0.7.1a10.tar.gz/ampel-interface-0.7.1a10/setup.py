# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ampel',
 'ampel.abstract',
 'ampel.alert',
 'ampel.base',
 'ampel.config',
 'ampel.content',
 'ampel.enum',
 'ampel.ingest',
 'ampel.model',
 'ampel.protocol',
 'ampel.struct',
 'ampel.util',
 'ampel.util.legacy',
 'ampel.view']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'pydantic>=1.4,<1.5', 'pymongo>=3.10,<4.0']

extras_require = \
{'docs': ['Sphinx>=3.5.1,<4.0.0',
          'sphinx-autodoc-typehints>=1.11.1,<2.0.0',
          'tomlkit>=0.7.0,<0.8.0']}

setup_kwargs = {
    'name': 'ampel-interface',
    'version': '0.7.1a10',
    'description': 'Base classes for the Ampel analysis platform',
    'long_description': '# Ampel-interface\n\n`ampel-interface` provides type-hinted abstract base classes for [Ampel](https://ampelproject.github.io).',
    'author': 'Valery Brinnel',
    'author_email': None,
    'maintainer': 'Jakob van Santen',
    'maintainer_email': 'jakob.van.santen@desy.de',
    'url': 'https://ampelproject.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
