# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weblustrator']

package_data = \
{'': ['*'], 'weblustrator': ['views/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'Pillow>=8.1.0,<9.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'bottle>=0.12.19,<0.13.0',
 'click>=7.1.2,<8.0.0',
 'livereload>=2.6.3,<3.0.0',
 'pyppeteer>=0.2.5,<0.3.0',
 'pypugjs>=5.9.8,<6.0.0',
 'python-frontmatter>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'weblustrator',
    'version': '0.1.2',
    'description': 'Generate illustrations using web technologies, such as svg, css, and javascript.',
    'long_description': None,
    'author': 'RCJacH',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
