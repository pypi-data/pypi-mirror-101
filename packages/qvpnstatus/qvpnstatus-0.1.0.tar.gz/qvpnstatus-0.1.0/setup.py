# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/main/python'}

packages = \
['qvpnstatus']

package_data = \
{'': ['*'], 'qvpnstatus': ['images/*', 'sounds/*']}

install_requires = \
['PyQt5-sip==12.8.1',
 'PyQt5-stubs==5.14.2.2',
 'PyQt5==5.15.2',
 'fbs==0.9.0',
 'nmcli>=0.5.0,<0.6.0',
 'psutil>=5.8.0,<6.0.0']

entry_points = \
{'console_scripts': ['qvpnstatus = qvpnstatus.main:main',
                     'qvpnstatuscli = qvpnstatus.cli:main']}

setup_kwargs = {
    'name': 'qvpnstatus',
    'version': '0.1.0',
    'description': 'VPN Status tray icon for monitoring VPN connection',
    'long_description': '# QVpnStatus\n\n[![pipeline status](https://gitlab.com/mikeramsey/qvpnstatus/badges/master/pipeline.svg)](https://gitlab.com/mikeramsey/qvpnstatus/pipelines)\n[![coverage report](https://gitlab.com/mikeramsey/qvpnstatus/badges/master/coverage.svg)](https://gitlab.com/mikeramsey/qvpnstatus/commits/master)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://mikeramsey.gitlab.io/qvpnstatus/)\n[![pypi version](https://img.shields.io/pypi/v/qvpnstatus.svg)](https://pypi.org/project/qvpnstatus/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/qvpnstatus/community)\n\nVPN Status tray icon for monitoring VPN connections from nmcli. Allows you to specify interval to check and also toggle off sound notifications.\n\n## Requirements\n\nQVpnStatus requires Python 3.7 or above.\n\n<details>\n<summary>To install Python 3.7, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.7\npyenv install 3.7.12\n\n# make it available globally\npyenv global system 3.7.12\n```\n</details>\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install qvpnstatus\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.6 -m pip install --user pipx\n\npipx install --python python3.6 qvpnstatus\n```\n',
    'author': 'Michael Ramsey',
    'author_email': 'mike@hackerdise.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mikeramsey/qvpnstatus',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
