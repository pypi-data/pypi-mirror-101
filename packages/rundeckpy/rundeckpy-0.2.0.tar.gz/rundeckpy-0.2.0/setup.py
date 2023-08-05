# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rundeckpy']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=2.7.2,<3.0.0']

setup_kwargs = {
    'name': 'rundeckpy',
    'version': '0.2.0',
    'description': 'Base class for python based Rundeck plugin',
    'long_description': '#rundeckpy\nBase class for python based Rundeck plugin.\n',
    'author': 'Thiago Takayama',
    'author_email': 'thiago@takayama.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/labitup/rundeck/rundeckpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
