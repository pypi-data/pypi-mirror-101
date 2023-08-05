# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastenv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fastenv',
    'version': '0.0.1',
    'description': 'Unified settings management for FastAPI and beyond.',
    'long_description': '# fastenv\n\n🔧 _Unified settings management for FastAPI and beyond_ 🚀\n\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![ci](https://github.com/br3ndonland/fastenv/workflows/ci/badge.svg)](https://github.com/br3ndonland/fastenv/actions/workflows/ci.yml)\n\n🚧 UNDER CONSTRUCTION - NOT FOR PRODUCTION 🚧\n\n## Description\n\n[Environment variables](https://en.wikipedia.org/wiki/Environment_variable) are key-value pairs provided to the operating system with syntax like `VARIABLE_NAME=value`. Collections of environment variables are stored in files commonly named _.env_ and called "dotenv" files. The Python standard library provides tools for reading environment variables, such as `os.getenv("VARIABLE_NAME")`, but these tools only read environment variables that have already been loaded. Additional logic is therefore needed to load environment variables before they can be read by Python.\n\nThis project aims to:\n\n- **Unify settings management for FastAPI**. [Uvicorn](https://www.uvicorn.org/), [Starlette](https://www.starlette.io/config/), and _[pydantic](https://pydantic-docs.helpmanual.io/usage/settings/)_ each have their own ways of loading environment variables and configuring application settings. This means that, when [configuring a FastAPI application](https://fastapi.tiangolo.com/advanced/settings/), there are at least three different settings management tools available, each with their own pros and cons. It would be helpful to address the limitations of each of these options, potentially providing a similar, improved API for each one.\n- **Replace the aging [python-dotenv](https://github.com/theskumar/python-dotenv) project** with a similar, but more intuitive API, and modern syntax and tooling.\n- **Read settings from TOML**. [It\'s all about _pyproject.toml_ now](https://snarky.ca/what-the-heck-is-pyproject-toml/). [Poetry](https://python-poetry.org/) has pushed [PEP 517](https://www.python.org/dev/peps/pep-0517/) build tooling and [PEP 518](https://www.python.org/dev/peps/pep-0518/) build requirements forward, and even `setuptools` has [come around](https://setuptools.readthedocs.io/en/latest/build_meta.html). Why don’t we use the metadata from our _pyproject.toml_ files in our Python APIs?\n- **Integrate with object storage**. Dotenv files are commonly kept in object storage like AWS S3, but none of the tools mentioned above integrate with object storage clients.\n\nLet\'s see how this goes!\n\n## Further information\n\nSee [CONTRIBUTING.md](.github/CONTRIBUTING.md).\n',
    'author': 'Brendon Smith',
    'author_email': 'br3ndonland@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/br3ndonland/fastenv',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
