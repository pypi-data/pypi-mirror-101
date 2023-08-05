# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weather_for_prebas_1']

package_data = \
{'': ['*']}

install_requires = \
['geopandas>=0.9.0,<0.10.0', 'requests>=2.25.1,<3.0.0', 'utm>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'weather-for-prebas-1',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jan Pisl',
    'author_email': 'jan.pisl@simosol.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
