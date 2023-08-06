# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flowdyn', 'flowdyn.modelphy', 'flowdyn.solution']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.15,<2.0']

setup_kwargs = {
    'name': 'flowdyn',
    'version': '1.1.1',
    'description': 'Model of discretization of hyperbolic model, base is Finite Volume method',
    'long_description': None,
    'author': 'j.gressier',
    'author_email': 'jeremie.gressier@isae-supaero.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jgressier/flowdyn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
