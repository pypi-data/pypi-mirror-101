# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['symphony',
 'symphony.bdk',
 'symphony.bdk.core',
 'symphony.bdk.core.activity',
 'symphony.bdk.core.auth',
 'symphony.bdk.core.client',
 'symphony.bdk.core.config',
 'symphony.bdk.core.config.model',
 'symphony.bdk.core.service',
 'symphony.bdk.core.service.application',
 'symphony.bdk.core.service.connection',
 'symphony.bdk.core.service.connection.model',
 'symphony.bdk.core.service.datafeed',
 'symphony.bdk.core.service.health',
 'symphony.bdk.core.service.message',
 'symphony.bdk.core.service.presence',
 'symphony.bdk.core.service.session',
 'symphony.bdk.core.service.signal',
 'symphony.bdk.core.service.stream',
 'symphony.bdk.core.service.user',
 'symphony.bdk.core.service.user.model',
 'symphony.bdk.gen',
 'symphony.bdk.gen.agent_api',
 'symphony.bdk.gen.agent_model',
 'symphony.bdk.gen.auth_api',
 'symphony.bdk.gen.auth_model',
 'symphony.bdk.gen.login_api',
 'symphony.bdk.gen.login_model',
 'symphony.bdk.gen.pod_api',
 'symphony.bdk.gen.pod_model']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.0.1,<3.0.0',
 'aiohttp>=3.7.3,<4.0.0',
 'cryptography>=3.4.6,<4.0.0',
 'nulltype>=2.3.1,<3.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'urllib3>=1.26.2,<2.0.0']

setup_kwargs = {
    'name': 'sym-api-client-python',
    'version': '2.0b1',
    'description': 'Symphony Bot Development Kit for Python',
    'long_description': '[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n[![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue)](https://www.python.org/downloads/release/python-3)\n[![Pypi](https://img.shields.io/badge/pypi-2.0b0-green)](https://pypi.org/project/sym-api-client-python/2.0b0/)\n![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/SymphonyPlatformSolutions/symphony-api-client-python/build/2.0)\n\n# Symphony BDK for Python\n\nThis is the Symphony BDK for Python to help develop bots and interact with the [Symphony REST APIs](https://developers.symphony.com/restapi/reference).\n\nLegacy Python BDK is located in [legacy](./legacy) folder.\n\n## Installation and getting started\nThe [reference documentation](https://symphonyplatformsolutions.github.io/symphony-api-client-python/) includes detailed\ninstallation instructions as well as a comprehensive\n[getting started](https://symphonyplatformsolutions.github.io/symphony-api-client-python/markdown/getting_started.html)\nguide.\n\n## Build from source\n\nThe Symphony BDK uses and requires Python 3.8 or higher. Be sure you have it installed before going further.\n\nWe use [poetry](https://python-poetry.org/) in order to manage dependencies, build, run tests and publish.\nTo install poetry, follow instructions [here](https://python-poetry.org/docs/#installation).\n\nOn the first time, run `poetry install`. Then run `poetry build` to build the sdist and wheel packages.\nTo run the tests, use `poetry run pytest`.\n\nIt is possible to run pylint scan locally (on a specific file or package) executing the following command:\n`poetry run pylint <module_name>`.\n\nTo generate locally the Sphinx documentation, run: `cd docsrc && make html`.\n\n## Contributing\n\nIf you want to contribute, please check the [contributing guidelines](CONTRIBUTING.md).',
    'author': 'Symphony Platform Solutions',
    'author_email': 'platformsolutions@symphony.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
