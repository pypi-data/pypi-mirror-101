# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['outcome', 'outcome.pypicloud_storage_gcs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'outcome-pypicloud-storage-gcs',
    'version': '0.3.0',
    'description': 'A fork-safe verion of the GCS Storage backend for PyPICloud.',
    'long_description': "# pypicloud-storage-gcs-py\n![Continuous Integration](https://github.com/outcome-co/pypicloud-storage-gcs-py/actions/workflows/ci.py.opensource.yaml/badge.svg) ![version-badge](https://img.shields.io/badge/version-0.3.0-brightgreen)\n\nA fork-safe verion of the GCS Storage backend.\n\nThe GCS library uses `requests` to handle HTTP/S calls, but the SSL-state management inside `requests` doesn't handle os.fork calls very well. By default, the pypicloud GCS storage adapter creates the client before forking, so the same GCS client gets used across multiple processes which leads to issues.\n\nThis replacement defers the creation of the GCS client until the process has been forked.\n\n## Usage\n\n### Installation\n\n```sh\npoetry add outcome-pypicloud-storage-gcs\n```\n\n### Configuration\n\nTo use the storage backend, configure it in the `server.ini`. The settings/options for the adapter are identical to those for the original adapter.\n\n```ini\n# Set up GCS storage\npypi.storage = outcome.pypicloud_storage_gcs.ThreadsafeGoogleCloudStorage\nstorage.bucket = my-bucket\n```\n\n## Development\n\nRemember to run `./pre-commit.sh` when you clone the repository.\n",
    'author': 'Outcome Engineering',
    'author_email': 'engineering@outcome.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcome-co/pypicloud-storage-gcs-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
