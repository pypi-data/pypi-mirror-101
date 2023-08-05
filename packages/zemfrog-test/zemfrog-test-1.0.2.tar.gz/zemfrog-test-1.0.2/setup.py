# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zemfrog_test', 'zemfrog_test.templates', 'zemfrog_test.templates.tests']

package_data = \
{'': ['*'], 'zemfrog_test.templates.tests': ['apis/*', 'blueprints/*']}

install_requires = \
['pytest>=6.2.2,<7.0.0', 'zemfrog>=4.0.5,<5.0.0']

entry_points = \
{'pytest11': ['zemfrog_test = zemfrog_test.fixtures']}

setup_kwargs = {
    'name': 'zemfrog-test',
    'version': '1.0.2',
    'description': 'Zemfrog unit testing tools',
    'long_description': None,
    'author': 'aprilahijriyan',
    'author_email': 'hijriyan23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
