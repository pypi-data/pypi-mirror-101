# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vigilant_crypto_snatch']

package_data = \
{'': ['*'], 'vigilant_crypto_snatch': ['templates/*']}

install_requires = \
['BitstampClient>=2.2.8,<3.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'clikraken>=0.8.3,<0.9.0',
 'coloredlogs>=15.0,<16.0',
 'pyyaml>=5.4.1,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'sqlalchemy>=1.3.23,<2.0.0',
 'urllib3>=1.26.3,<2.0.0']

extras_require = \
{'evaluation': ['pandas>=1.2.3,<2.0.0',
                'matplotlib>=3.3.4,<4.0.0',
                'tqdm>=4.59.0,<5.0.0',
                'Markdown>=3.3.4,<4.0.0',
                'scipy>=1.6.2,<2.0.0']}

entry_points = \
{'console_scripts': ['vigilant-crypto-snatch = '
                     'vigilant_crypto_snatch.cli:main']}

setup_kwargs = {
    'name': 'vigilant-crypto-snatch',
    'version': '3.0.3',
    'description': 'Crypto currency buying agent',
    'long_description': None,
    'author': 'Martin Ueding',
    'author_email': 'mu@martin-ueding.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
