# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cepan']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.19,<2.0.0', 'pandas>=1.2.3,<2.0.0']

setup_kwargs = {
    'name': 'cepan',
    'version': '0.2.0',
    'description': 'Retrieves data from aws cost explore as a pandas dataframe.',
    'long_description': '# cepan\n\n[![Pypi Version](https://img.shields.io/pypi/v/cepan?color=blue)](https://pypi.org/project/cepan/#history)\n[![python](https://img.shields.io/pypi/pyversions/cepan.svg)](https://pypi.org/project/cepan/)\n[![test](https://github.com/kanga333/cepan/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/kanga333/cepan/actions/workflows/test.yml)\n[![lint](https://github.com/kanga333/cepan/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/kanga333/cepan/actions/workflows/lint.yml)\n[![Code style: black](https://img.shields.io/badge/mypy-checked-blue.svg)](http://mypy-lang.org/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n\nRetrieves data from aws cost explore as a pandas dataframe.\n\nMain features\n- Support for input with type hints\n- Retrieving results as pandas.Dataframe\n\n## Installation\n\n```\npip install cepan\n```\n\n## Usage\n\n```python\nfrom datetime import datetime\n\nimport cepan as ce\n\ndf = ce.get_cost_and_usage(\n    time_period=ce.TimePeriod(\n        start=datetime(2020, 1, 1),\n        end=datetime(2020, 1, 2),\n    ),\n    granularity="DAILY",\n    filter=ce.And(\n        [\n            ce.Dimensions(\n                "SERVICE",\n                ["Amazon Simple Storage Service", "AmazonCloudWatch"],    \n            ),\n            ce.Tags("Stack", ["Production"]),\n        ]\n    ),\n    metrics=["BLENDED_COST"],\n    group_by=ce.GroupBy(\n        dimensions=["SERVICE", "USAGE_TYPE"],\n    ),\n)\nprint(df)\n```\n\nAll paginated results will be returned as a Dataframe.\n\n```\n          Time                        SERVICE  BlendedCost\n0   2020-01-01  Amazon Simple Storage Service   100.000000\n1   2020-01-01               AmazonCloudWatch    10.000000\n```\n\n### List of currently supported APIs\n\n- get_dimension_values\n- get_tags\n- get_cost_and_usage\n\n### Alias of aws service name\n\nNormally, the Cost Explorer API requires complex and long names to filter by service name.\nFor example, if you only need the value of an EC2 instance, you would need to specify `Amazon Elastic Compute Cloud - Compute`.\n\n```python\ndf = ce.get_cost_and_usage(\n    time_period=ce.TimePeriod(\n        start=datetime(2020, 1, 1),\n        end=datetime(2020, 1, 2),\n    ),\n    granularity="DAILY",\n    filter=ce.Dimensions(\n        "SERVICE",\n        ["Amazon Elastic Compute Cloud - Compute"],    \n    ),\n    group_by=ce.GroupBy(\n        dimensions=["SERVICE", "USAGE_TYPE"],\n    ),\n)\n```\n\ncepan supports aliases with short service names.\nIf you only need the value of the EC2 instance, you can specify it with  `EC2`.\n\n```python\ndf = ce.get_cost_and_usage(\n    time_period=ce.TimePeriod(\n        start=datetime(2020, 1, 1),\n        end=datetime(2020, 1, 2),\n    ),\n    granularity="DAILY",\n    filter=ce.Dimensions(\n        "SERVICE",\n        ["EC2"],    \n    ),\n    group_by=ce.GroupBy(\n        dimensions=["SERVICE", "USAGE_TYPE"],\n    ),\n)\n```\n\nCorrespondence table of aliases is shown in [service_alias.tsv](service_alias.tsv).\nYou can also run the `show_service_alias` method to get the table.\n\n```python\nprint(ce.show_service_alias())\n```\n\n## License\n\nMIT License\n',
    'author': 'kanga333',
    'author_email': 'e411z7t40w@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kanga333/cepan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
