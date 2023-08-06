# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_favicon',
 'wagtail_favicon.migrations',
 'wagtail_favicon.templatetags']

package_data = \
{'': ['*'], 'wagtail_favicon': ['templates/*', 'templates/tags/*']}

install_requires = \
['Django>=2.2,<3.0', 'wagtail>=2.8,<3.0']

setup_kwargs = {
    'name': 'wagtail-favicon',
    'version': '0.1.5',
    'description': 'Easily add shortcut icons to any wagtail site.',
    'long_description': None,
    'author': 'Pat Horsley',
    'author_email': 'pat@octave.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
