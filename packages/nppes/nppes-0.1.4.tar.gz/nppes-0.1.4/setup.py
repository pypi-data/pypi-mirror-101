# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nppes']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.6.1,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'pandas>=1.1.2,<2.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['search_nppes_api = nppes.search:main']}

setup_kwargs = {
    'name': 'nppes',
    'version': '0.1.4',
    'description': "Package to interface with the Center for Medicare and Medicaid's (CMS) National Plan and Provider Enumeration System (NPPES).",
    'long_description': "# nppes\n\nPackage to interface with the Center for Medicare and Medicaid's (CMS) National Plan and Provider Enumeration System (NPPES).\n\n## To Install\n\n```\n$ pip install nppes\n\n```\n\n## Search\n\nTo search the NPPES API, simply search via your terminal.\n\n```\n$ search_nppes_api --first_name James --last_name Moore\n\n```\n\nTo search the NPPES API and put results into a DataFrame:\n\n```\nfrom nppes import nppes_df\n\ndf = nppes_df(first_name='James', last_name='Moore')\n\n```\n\nOptional arguments include:\n\n-   number\n-   enumeration_type\n-   taxonomy_description\n-   first_name\n-   last_name\n-   organization_name\n-   address_purpose\n-   city\n-   state\n-   postal_code\n-   limit\n\n## Development\n\nTo run all tests: \n\n    $ nox\n",
    'author': 'Jason Turan',
    'author_email': 'jason.turan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
