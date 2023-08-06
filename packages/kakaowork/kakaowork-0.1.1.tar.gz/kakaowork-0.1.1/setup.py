# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kakaowork']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=1.26.4,<2.0.0']

entry_points = \
{'console_scripts': ['kakaowork = kakaowork.__main__:main']}

setup_kwargs = {
    'name': 'kakaowork',
    'version': '0.1.1',
    'description': 'Kakaowork Python client',
    'long_description': '# Kakaowork\n\n[![CI](https://github.com/skyoo2003/kakaowork-py/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/skyoo2003/kakaowork-py/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/skyoo2003/kakaowork-py/branch/master/graph/badge.svg?token=J6NQHDJEMZ)](https://codecov.io/gh/skyoo2003/kakaowork-py)\n\n(Unofficial) Kakaowork Python client\n',
    'author': 'Sung-Kyu Yoo',
    'author_email': 'skyoo2003@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skyoo2003/kakaowork-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
