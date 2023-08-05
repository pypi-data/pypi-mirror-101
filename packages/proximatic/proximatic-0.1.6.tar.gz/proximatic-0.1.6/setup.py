# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proximatic']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['proximatic = proximatic.main:cli',
                     'proximatic-http = proximatic.runhttp:http']}

setup_kwargs = {
    'name': 'proximatic',
    'version': '0.1.6',
    'description': 'Python API and CLI for managing Proximatic configuration.',
    'long_description': "# Proximatic\n\nPython API for managing Proximatic configuration files.\n\nWhen installed, the `proximatic` command provides a CLI for managing Proximatic configuration.\n\nThis Python package provides the core for the Proximatic system.\n\n## Installation\n\n```bash\npip install proximatic\n```\n\n## Usage\n\n### Command Line Interface (CLI)\n\nOpen a Terminal and type:\n\n```bash\nproximatic\n```\n\nUse `proximatic --help` for available commands and options.\n\n### Python API programmatic interface\n\n```python\nfrom proximatic import Proximatic\nproximatic = Proximatic(yml_dir='/path/to/your/proximatic/data', fqdn='yourdomain.org')\n```\n\n### JSON REST API interface\n\nYou can run the (experimental) REST API on your localhost by typing the command:\n\n```bash\nproximatic-http\n```\n\nIt will try to open your browser to [http://localhost:8000](http://localhost:8000)\n\n## License\n\nThe MIT License (MIT)\n\n## Author\n\nLink Swanson (LunkRat)",
    'author': 'Link Swanson',
    'author_email': 'link@swanson.link',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
