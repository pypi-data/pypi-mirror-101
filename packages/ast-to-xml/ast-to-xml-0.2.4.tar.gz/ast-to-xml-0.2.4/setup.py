# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ast_to_xml']
install_requires = \
['lxml>=4.6.3,<5.0.0']

setup_kwargs = {
    'name': 'ast-to-xml',
    'version': '0.2.4',
    'description': 'Converts a Python abstract source tree (AST) to an XML representation. Uses lxml to enable full XPath searching.',
    'long_description': None,
    'author': 'Ellis Percival',
    'author_email': 'ast-to-xml@failcode.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
