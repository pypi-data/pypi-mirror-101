# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['easypyrequests']
setup_kwargs = {
    'name': 'easypyrequests',
    'version': '1.0.0',
    'description': 'Requests Library for easy format',
    'long_description': None,
    'author': 'DragonWolf',
    'author_email': 'officialdragonwolf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
