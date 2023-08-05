# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['supabase_py', 'supabase_py.lib']

package_data = \
{'': ['*']}

install_requires = \
['gotrue==0.2.0',
 'postgrest-py==0.4.0',
 'pytest>=6,<7',
 'realtime-py>=0.1.2,<0.2.0',
 'requests==2.25.1']

setup_kwargs = {
    'name': 'supabase-py',
    'version': '0.0.2',
    'description': 'Supabase client for Python.',
    'long_description': None,
    'author': 'Joel Lee',
    'author_email': 'joel@joellee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
