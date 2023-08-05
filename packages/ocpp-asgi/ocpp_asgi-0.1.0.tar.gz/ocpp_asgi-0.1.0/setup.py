# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ocpp_asgi']

package_data = \
{'': ['*']}

install_requires = \
['ocpp>=0.8.1,<0.9.0']

setup_kwargs = {
    'name': 'ocpp-asgi',
    'version': '0.1.0',
    'description': 'ocpp-asgi extends ocpp library to provide ASGI compliant interface.',
    'long_description': None,
    'author': 'Ville Kärkkäinen',
    'author_email': 'ville.karkkainen@etteplan.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.1',
}


setup(**setup_kwargs)
