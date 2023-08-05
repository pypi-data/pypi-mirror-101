# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_sessions', 'fastapi_sessions.backends', 'fastapi_sessions.typings']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0', 'itsdangerous>=1.1.0,<2.0.0']

extras_require = \
{'dev': ['flake8>=3.9.0,<4.0.0',
         'flake8-docstrings>=1.6.0,<2.0.0',
         'black>=20.8b1,<21.0',
         'uvicorn[standard]>=0.13.4,<0.14.0',
         'pytest>=6.2.3,<7.0.0'],
 'docs': ['mkdocs-material>=7.1.0,<8.0.0', 'markdown-include>=0.6.0,<0.7.0']}

setup_kwargs = {
    'name': 'fastapi-sessions',
    'version': '0.1.0',
    'description': 'Ready-to-use session cookies with custom backends for FastAPI',
    'long_description': '# FastAPI-Sessions\n\n\n\n---\n\nDocumentation: [https://jordanisaacs.github.io/fastapi-sessions/](https://jordanisaacs.github.io/fastapi-sessions/)\n\nSource Code: [https://github.com/jordanisaacs/fastapi-sessions/](https://github.com/jordanisaacs/fastapi-sessions/)\n\n---\n\nQuickly add session authentication to your FastAPI project. **FastAPI Sessions** is designed to be user friendly and customizable.\n\n\n## Features\n\n- [x] Dependency injection to protect the routes you want\n- [x] Timestamp signed session IDs with [itsdangerous](https://itsdangerous.palletsprojects.com/en/1.1.x/)\n- [x] Compabitibility with OpenAPI docs using [APIKeyCookie](https://swagger.io/docs/specification/authentication/cookie-authentication/)\n- [x] Pydantic models for verifying session data\n- [x] Abstract session backend so you can build one that fits your needs\n- [x] Currently included backends\n    - [x] In memory\n\nNotes:\n\n* Currently working on CSRF tokens\n* Plan is to implement more backends\n\n## Installation\n\n```py\npip install fastapi-sessions\n```\n\n## Guide\n\nCheck out the guide to building and using session based authentication with fastapi-sessions: [https://jordanisaacs.github.io/fastapi-sessions/guide/getting_started/]()\n',
    'author': 'Jordan Isaacs',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jordanisaacs/fastapi-sessions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
