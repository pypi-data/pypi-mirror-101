# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['materia',
 'materia.actions',
 'materia.dataseries',
 'materia.engines',
 'materia.molecule',
 'materia.symmetry']

package_data = \
{'': ['*']}

install_requires = \
['PubChemPy>=1.0.4,<2.0.0',
 'cclib>=1.6.4,<2.0.0',
 'dask-jobqueue>=0.7.2,<0.8.0',
 'dask>=2020.12.0,<2021.0.0',
 'dlib>=19.21.1,<20.0.0',
 'networkx>=2.5,<3.0',
 'numpy>=1.19.4,<2.0.0',
 'scipy>=1.5.4,<2.0.0',
 'spglib>=1.16.0,<2.0.0']

setup_kwargs = {
    'name': 'materia',
    'version': '9.1.2',
    'description': 'Module for integrated materials simulations.',
    'long_description': '==============\nMateria Module\n==============\n\n.. image:: https://codecov.io/gh/kijanac/materia/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/kijanac/materia\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github\n\n**Module for integrated materials simulations.**\n\nLonger description coming soon!\n\n---------------\nGetting Started\n---------------\n\nPrerequisites\n-------------\n\nInstalling\n----------\n\nTo install, open a shell terminal and run::\n\n`conda create -n materia -c conda-forge -c kijana materia`\n\n----------\nVersioning\n----------\n\n-------\nAuthors\n-------\n\nKi-Jana Carter\n\n-------\nLicense\n-------\nThis project is licensed under the MIT License - see the LICENSE file for details.\n',
    'author': 'Ki-Jana Carter',
    'author_email': 'kijana@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kijanac/luz',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
