# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoname']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'autoname',
    'version': '1.0.0',
    'description': 'an enum `AutoName` from python docs with multiple stringcase options',
    'long_description': '# This project is archived. I find StrEnum, fastapi-utils is better.\n\nI removed autoname from pypi\n\n# autoname\n\n\n\nan enum `AutoName` from [python docs](https://docs.python.org/3/library/enum.html#using-automatic-values) with multiple stringcase options.\n\n## Get Started\n\n```bash\n$ pip install autoname\n```\n\n```python\nfrom autoname import Autoname\nfrom enum import auto\n\n# an enum class\nclass GameType(AutoName):\n    INDIE = auto()\n\nprint(GameType.INDIE.value) # "INDIE"\n\n# could be alternative in pydantic instead of literal\nfrom pydantic import BaseModel\nclass Game(BaseModel):\n    type: GameType\n```\n\nAlso have others stringcases coverter\n1. `AutoNameLower` - convert name value to lowercase\n2. `AutoNameUpper` - convert name value to uppercase\n\ne.g.\n```python\nclass GameType(AutoNameLower):\n    INDIE = auto()\n\nprint(GameType.INDIE.value) # "indie"\n```\n',
    'author': 'Nutchanon Ninyawee',
    'author_email': 'me@nutchanon.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CircleOnCircles/autoname',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
