# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keras_data_format_converter',
 'keras_data_format_converter.layers',
 'keras_data_format_converter.layers.confighandlers']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow-addons>=0.12.1,<0.13.0', 'tensorflow>=2.4.1,<3.0.0']

setup_kwargs = {
    'name': 'keras-data-format-converter',
    'version': '0.0.6a0',
    'description': '',
    'long_description': None,
    'author': 'dorhar',
    'author_email': 'doron.harnoy@tensorleap.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.8,<4.0.0',
}


setup(**setup_kwargs)
