# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['http_inspector', 'http_inspector.logger']

package_data = \
{'': ['*']}

install_requires = \
['rich>=10.0.1,<11.0.0']

entry_points = \
{'console_scripts': ['hyper = http_inspector.__main__:main']}

setup_kwargs = {
    'name': 'hyper-inspector',
    'version': '0.0.2',
    'description': 'A simple HTTP inspector to debug webhooks and other incoming requests',
    'long_description': 'A dummy/mocking server to inspect incoming HTTP connections. Use it to test/debug Webhooks.\n\n### Installation\n\n```bash\n```\n\n### Usage\n\n```\n```\n',
    'author': 'Santiago Basulto',
    'author_email': 'santiago.basulto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
