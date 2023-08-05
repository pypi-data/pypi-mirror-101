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
    'version': '0.1.2',
    'description': 'VPN Status tray icon for monitoring VPN connection',
    'long_description': '# QVpnStatus\n\n[![pipeline status](https://gitlab.com/mikeramsey/qvpnstatus/badges/master/pipeline.svg)](https://gitlab.com/mikeramsey/qvpnstatus/pipelines)\n[![coverage report](https://gitlab.com/mikeramsey/qvpnstatus/badges/master/coverage.svg)](https://gitlab.com/mikeramsey/qvpnstatus/commits/master)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://mikeramsey.gitlab.io/qvpnstatus/)\n[![pypi version](https://img.shields.io/pypi/v/qvpnstatus.svg)](https://pypi.org/project/qvpnstatus/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/qvpnstatus/community)\n\nVPN Status tray icon for monitoring VPN connections from nmcli. Allows you to specify interval to check and also toggle off sound notifications.\n\nSee link [here](https://wizardassistant.com/qvpn-status-monitor-status-and-restart-vpn-connections-in-linux/) for more information.\n\nIt is based on my [copier-poetry-fbs](https://gitlab.com/mikeramsey/copier-poetry-fbs) skeleton which uses PyQT5 for the GUI elements and [fbs](https://github.com/mherrmann/fbs) for the installer creation.\n\n\n## Installation\n\n###Debian/Ubuntu/Mint Linux Installation\n\nManual Installer link without automatic updates.\nhttps://fbs.sh/qvpnstatus/qvpnstatus/qvpnstatus.deb\n\n###Install from website.\n```bash\nwget https://fbs.sh/qvpnstatus/qvpnstatus/qvpnstatus.deb\nsudo dpkg -i qvpnstatus.deb\n```\n####To install with automatic updates supported via repo.\n```bash\nsudo apt-get install -y apt-transport-https\nwget -qO - https://fbs.sh/qvpnstatus/qvpnstatus/public-key.gpg | sudo apt-key add -\necho \'deb [arch=amd64] https://fbs.sh/qvpnstatus/qvpnstatus/deb stable main\' | sudo tee /etc/apt/sources.list.d/qvpnstatus.list\nsudo apt-get update; sudo apt-get install -y qvpnstatus\n```\nInstallation is done into /opt/qvpnstatus/   \n\n--------------------------------------------------------------------------\n\n###Arch Linux Installation\n\n####Manual Installer link without automatic updates.\nhttps://fbs.sh/qvpnstatus/qvpnstatus/qvpnstatus.pkg.tar.xz\n\n####To install with automatic updates supported via repo.\n```bash\ncurl -O https://fbs.sh/qvpnstatus/qvpnstatus/public-key.gpg && sudo pacman-key --add public-key.gpg && sudo pacman-key --lsign-key 9EF5FD1B7714354D0535303CFF1B29F26A1378E8 && rm public-key.gpg\necho -e \'\\n[qvpnstatus]\\nServer = https://fbs.sh/qvpnstatus/qvpnstatus/arch\' | sudo tee -a /etc/pacman.conf\nsudo pacman -Syu qvpnstatus\n```\nIf you already have the app installed, you can force an immediate update via:\n```bash\nsudo pacman -Syu --needed qvpnstatus\n```\n\n--------------------------------------------------------------------------\n\n## Installation via `pip`:\n```bash\npython3.7 -m pip install qvpnstatus\n```\n\nInstallation via [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.7 -m pip install --user pipx\n\npipx install --python python3.7 qvpnstatus\n```\n\n## Dev Requirements\n\nQVpnStatus requires Python 3.7 or above.\n\n<details>\n<summary>To install Python 3.7, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.7\npyenv install 3.7.12\n\n# make it available globally\npyenv global system 3.7.12\n```\n</details>\n\n\n## Creating a native installer\n-  clone the repo locally   \n   `git clone git@gitlab.com:mikeramsey/qvpnstatus.git`\n-  Install [poetry](https://python-poetry.org/)   \n   `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -`   \n-  Setting the below settings are highly recommended for ensuring the virtual environment poetry makes is located inside the project folder.    \n   `poetry config virtualenvs.create true; poetry config virtualenvs.in-project true;`\n-  Run `poetry install` in the path to install all the dependencies\n-  Enter the virtual environment that poetry created. This can be found by running `poetry env info` See also [here](https://python-poetry.org/docs/managing-environments/)\n-  Run `fbs freeze` and then `fbs installer` afterwards if the frozen "compiled" app runs without issues. See [here](https://github.com/mherrmann/fbs-tutorial) for more on how fbs works. And also [here](https://www.learnpyqt.com/tutorials/packaging-pyqt5-apps-fbs/)\n\n## Credits\nSpecial thanks to below references and resources.\n\nResources:\nPython nmcli api package which made this a breeze:   \nhttps://github.com/ushiboy/nmcli   \nhttps://pypi.org/project/nmcli/\n\nReferences:  \nhttps://www.learnpyqt.com/tutorials/system-tray-mac-menu-bar-applications-pyqt/   \nhttps://itectec.com/ubuntu/ubuntu-connect-disconnect-from-vpn-from-the-command-line/   \nhttps://www.devdungeon.com/content/python3-qt5-pyqt5-tutorial#toc-9   ',
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
