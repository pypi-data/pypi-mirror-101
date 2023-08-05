# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyspark_spy']

package_data = \
{'': ['*']}

install_requires = \
['pyspark>=2.0.0']

setup_kwargs = {
    'name': 'pyspark-spy',
    'version': '1.0',
    'description': 'Collect and aggregate on spark events for profitz. In 🐍 way!',
    'long_description': None,
    'author': 'Alexander Gorokhov',
    'author_email': 'sashgorokhov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
