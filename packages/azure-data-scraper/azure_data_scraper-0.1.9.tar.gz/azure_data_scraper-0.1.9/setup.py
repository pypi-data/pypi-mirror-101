# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azure_data_scraper']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'lxml>=4.6.2,<5.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'azure-data-scraper',
    'version': '0.1.9',
    'description': '',
    'long_description': '[![01 Tests](https://github.com/timothymeyers/azure-data-scraper/actions/workflows/unit-test.yml/badge.svg)](https://github.com/timothymeyers/azure-data-scraper/actions/workflows/unit-test.yml)\n\n[![02 Publish to Test PyPi](https://github.com/timothymeyers/azure-data-scraper/actions/workflows/publish-to-test.yml/badge.svg)](https://github.com/timothymeyers/azure-data-scraper/actions/workflows/publish-to-test.yml)\n\n[![03 Publish to PyPi](https://github.com/timothymeyers/azure-data-scraper/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/timothymeyers/azure-data-scraper/actions/workflows/publish-to-pypi.yml)\n\n[![codecov](https://codecov.io/gh/timothymeyers/azure-data-scraper/branch/main/graph/badge.svg?token=F0PCFFPNDT)](https://codecov.io/gh/timothymeyers/azure-data-scraper)\n\n[![PyPI version](https://badge.fury.io/py/azure-data-scraper.svg)](https://badge.fury.io/py/azure-data-scraper)\n\n# azure-data-scraper\ntbd\n\n',
    'author': 'Tim Meyers',
    'author_email': 'timothy.m.meyers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
