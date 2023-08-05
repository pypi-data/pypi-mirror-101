# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_tutorial_project_doron']

package_data = \
{'': ['*']}

install_requires = \
['icecream>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'poetry-tutorial-project-doron',
    'version': '0.3.1a2',
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
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
