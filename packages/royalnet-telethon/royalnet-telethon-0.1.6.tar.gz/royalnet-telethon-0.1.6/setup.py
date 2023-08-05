# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalnet_telethon',
 'royalnet_telethon.bullet.contents',
 'royalnet_telethon.bullet.projectiles']

package_data = \
{'': ['*']}

install_requires = \
['Telethon>=1.21.1,<2.0.0', 'royalnet>=6.1.2,<7.0.0']

setup_kwargs = {
    'name': 'royalnet-telethon',
    'version': '0.1.6',
    'description': 'A Telethon-based frontend for the royalnet.engineer module.',
    'long_description': '# `royalnet_console`\n\nA terminal-based frontend for the `royalnet.engineer` module.\n\nThe documentation is [hosted on Read The Docs](https://royalnet-console.readthedocs.io/en/latest/).\n\n## See also\n\n- [Royalnet 6](https://github.com/Steffo99/royalnet-6)\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Steffo99/royalnet-telethon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
