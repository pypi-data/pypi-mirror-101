# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pfun']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.2,<0.4.0', 'typing-extensions>=3.7,<4.0']

extras_require = \
{'http': ['aiohttp[speedups]>=3.7.4,<4.0.0'],
 'sql': ['asyncpg>=0.20.1,<0.21.0']}

setup_kwargs = {
    'name': 'pfun',
    'version': '0.12.0',
    'description': '',
    'long_description': '## <img src="https://raw.githubusercontent.com/suned/pfun/master/logo/pfun_logo.svg?sanitize=true" style=" width:50px ; height:50px "/> <br> <p align="center">Functional, composable, asynchronous, type-safe Python.</p>\n\n- [Documentation](https://pfun.dev)\n- [Known issues](https://github.com/suned/pfun/issues?q=is%3Aopen+is%3Aissue+label%3Abug)\n\n## Install\n\n```console\n$ pip install pfun\n```\n\nOr with optional dependencies:\n```console\n$ pip install pfun[http,sql]\n```\n\n## Resources\n\n### Articles\n- [Purely Functional Python With Static Types](https://dev.to/suned/purely-functional-python-with-static-types-41mf)\n- [Be More Lazy, Become More Productive](https://dev.to/suned/be-more-lazy-become-more-productive-2cnb)\n- [Completely Type-Safe Error Handling in Python](https://dev.to/suned/completely-type-safe-error-handling-in-python-3apg)\n- [Completely Type-Safe Dependency Injection in Python](https://dev.to/suned/completely-type-safe-dependency-injection-in-python-48a5)\n\n### Examples\n- [Todo-Backend](https://github.com/suned/pfun-todo-backend/) (implementation of [todobackend.com](https://todobackend.com/))\n## Support\n\nOn [ko-fi](https://ko-fi.com/python_pfun)\n\n## Development\n\nRequires [poetry](https://poetry.eustace.io/)\n\n- Install dependencies with `poetry install -E http -E sql`\n- Build documentation with `poetry run task serve-docs`\n- Run tests with `poetry run task test`\n- Lint with `poetry run task lint`\n',
    'author': 'Sune Debel',
    'author_email': 'sad@archii.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
