# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['keyhint', 'keyhint.config', 'keyhint.resources']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.40.0,<4.0.0', 'PyYAML>=5.4.1,<6.0.0']

entry_points = \
{'console_scripts': ['keyhint = keyhint.app:main']}

setup_kwargs = {
    'name': 'keyhint',
    'version': '0.2.0',
    'description': 'Cheat-sheets for shortcuts & commands at your fingertips.',
    'long_description': '# KeyHint\n\n**_Display keyboard shortcuts or other hints based on the the active window. (GTK, Linux only!)_**\n\n<p align="center"><br>\n<img alt="Tests passing" src="https://github.com/dynobo/keyhint/workflows/Test/badge.svg">\n<a href="https://github.com/dynobo/keyhint/blob/master/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/Code%20style-black-%23000000"></a>\n<a href=\'https://coveralls.io/github/dynobo/keyhint\'><img src=\'https://coveralls.io/repos/github/dynobo/keyhint/badge.svg\' alt=\'Coverage Status\' /></a>\n</p>\n\n<p align="center"><br><img src="https://raw.githubusercontent.com/dynobo/keyhint/master/src/keyhint/resources/keyhint_128.png"></p>\n\n## Usage\n\n- Install from **PyPi** with `pip install keyhint` and run `keyhint`.\n- _Or_ download the **AppImage** from [releases](https://github.com/dynobo/keyhint/releases), make it executable and run it.\n- Configure a **global hotkey** (e.g. `F1`) to start KeyHint on demand.\n\n_KeyHint with KeyBindings for VS Code:_\n\n![VS Code Shortcuts](https://raw.githubusercontent.com/dynobo/keyhint/master/src/keyhint/resources/vscode.png)\n\n## CLI Options\n\n```\nApplication Options:\n  -h, --hint=HINT-ID             Show hints by specified ID\n  -d, --default-hint=HINT-ID     Hint to show in case no hints for active application were found\n  -v, --verbose                  Verbose log output for debugging\n  --display=DISPLAY              X display to use\n```\n\n## Configuration\n\n- The **config directory** is `~/.config/keyhint/`.\n- To **customize existing** hints, copy [the corresponding .yaml-file](https://github.com/dynobo/keyhint/tree/master/src/keyhint/config) into the config directory. Make your changes in a text editor. As long as you don\'t change the `id` it will overwrite the defaults.\n- To **create new** hints, I suggest you also start with [one of the existing .yaml-file](https://github.com/dynobo/keyhint/tree/master/src/keyhint/config):\n  - Place it in the config directory and give it a good file name.\n  - Change the value `id` to something unique.\n  - Adjust `regex_process` and `regex_title` so it will be selected based on the active window. (See [Tips](#tips))\n  - Add the `hints` to be displayed. \n  - If you think the hints might be useful for others, please consider opening a pull request or an issue.\n- You can always **reset a configuration** to the shipped version by deleting the `.yaml` files from the config folder.\n\n## Tips\n\n**Hints selection:**\n\n- The hints to be displayed on startup are selected by comparing the value of `regex_process` with the wm_class of the active window and the value of `regex_title` with the title of the active window. \n- The potential hints are processed alphabetically by filename, the first file that matches both wm_class and title are gettin displayed. \n- Both of `regex_` values are interpreted as **case insensitive regular expressions**.\n- Check "Debug Info" in the application menu to get insights about the active window and the selected hints file.\n\n**Available hints:**\n\n- Check the [included yaml-files](https://github.com/dynobo/keyhint/tree/master/src/keyhint/config) to see wich applications are available by default.\n- Feel free submit additional `yaml-files` for further applications.\n\n**Differentiate hints per website:**\n\n- For showing different browser-hints depending on the current website, you might want to use a browser extension like "[Add URL To Window Title](https://addons.mozilla.org/en-US/firefox/addon/add-url-to-window-title/)" and then configure the sections in `hints.yaml` to look for the URL in the window title.\n\n## Contribute\n\nI\'m happy about any contribution! Especially I would appreciate submissions to improve the [shipped hints](https://github.com/dynobo/keyhint/tree/master/src/keyhint/config). (The current set are the hints I personally use).\n\n## Design Principles\n\n- **Don\'t run as service**<br>It shouldn\'t consume resources in the background, even if this leads to slower start-up time.\n- **No network connection**<br>Everything should run locally without any network communication.\n- **Dependencies**<br>The fewer dependencies, the better.\n- **Multi-Monitors**<br>Supports setups with two or more displays\n\n## Certification\n\n![WOMM](https://raw.githubusercontent.com/dynobo/lmdiag/master/badge.png)\n',
    'author': 'dynobo',
    'author_email': 'dynobo@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynobo/keyhint',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
