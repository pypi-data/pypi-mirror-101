# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wind_stats']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['Pint>=0.17.0,<0.18.0',
 'numpy>=1.19.4,<2.0.0',
 'scipy>=1.5.4,<2.0.0',
 'xarray>=0.17.0,<0.18.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0',
                             'importlib-metadata>=3.4.0,<4.0.0']}

setup_kwargs = {
    'name': 'wind-stats',
    'version': '0.2.0',
    'description': 'Statistics tools to evaluate your wind energy projects',
    'long_description': '<p align="center">\n  <a href="https://github.com/jules-ch/wind-stats"><img src="https://raw.githubusercontent.com/jules-ch/wind-stats/main/docs/_static/logo-wind-stats.png" alt="wind-stats"></a>\n</p>\n\n-----------------\n\n# Wind stats\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Tests](https://github.com/jules-ch/wind-stats/workflows/CI/badge.svg)](https://github.com/jules-ch/wind-stats/actions?query=workflow%3ACI)\n[![codecov](https://codecov.io/gh/jules-ch/wind-stats/branch/main/graph/badge.svg)](https://codecov.io/gh/jules-ch/wind-stats)\n[![PyPi Version](https://img.shields.io/pypi/v/wind-stats)](https://pypi.org/project/wind-stats)\n[![Supported Versions](https://img.shields.io/pypi/pyversions/wind-stats.svg)](https://pypi.org/project/wind-stats)\n[![License: MIT](https://raw.githubusercontent.com/jules-ch/wind-stats/main/docs/_static/license.svg)](https://github.com/jules-ch/wind-stats/blob/master/LICENSE)\n\n\nWind-stats is a package to easily compute power statistics for your wind energy projects.\n\n## Features\n\n- Read generalized wind climate (GWC) file from [Global Wind Atlas](https://globalwindatlas.info/).\n- Shelter model for wind speed reduction from obstacles.\n- Compute global Weibull parameters based on site location.\n\n- Get general statistics to compare different sites implementation (mean wind speed, mean power density).\n- Compute annual energy production based on wind turbine power curve & site\'s wind distribution.\n\n\n## Installation\n\n```console\npip install wind-stats\n```\n\n## Examples\n\nSee our examples on how to use \n\n## Ressources\n   - Troen, I., & Lundtang Petersen, E. (1989). European Wind Atlas. Risø National Laboratory.\n   - Peña, A., Bechmann, A., Conti, D., Angelou, N., & Troen, I. (2015). Shelter models and observations. DTU Wind\nEnergy. DTU Wind Energy E, No. 00923\n   - Marc Rapin , Philippe Leconte (2017). Évolution, principes de base et potentiel de conversion. Techniques de l\'ingénieur\n',
    'author': 'Jules Chéron',
    'author_email': 'jules.cheron@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jules-ch/wind-stats',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
