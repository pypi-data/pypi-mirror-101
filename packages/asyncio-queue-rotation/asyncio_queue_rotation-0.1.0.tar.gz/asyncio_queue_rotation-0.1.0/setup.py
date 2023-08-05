# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncio_queue_rotation']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asyncio-queue-rotation',
    'version': '0.1.0',
    'description': '',
    'long_description': '# asyncio rotation queue\n\nbased on [asyncio.Queue](https://docs.python.org/3/library/asyncio-queue.html)\n\nOn put( element )\nif qsize() >= maxsize  \nfirst element popped out and put elements added to back of queue\n\n```python\nfrom asyncio_queue_rotation import RotationQueue\n\nrotation_queue = RotationQueue(10)\nawait rotation_queue.put(1)\n\n```\n',
    'author': 'und3v3l0p3d',
    'author_email': 'prohibitme@phygitalism.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/und3v3l0p3d/asyncio-rotation',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
