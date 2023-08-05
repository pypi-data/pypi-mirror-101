# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stb', 'stb.cli', 'stb.core']

package_data = \
{'': ['*'], 'stb': ['config/*']}

install_requires = \
['PyGObject>=3.40.0,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'config-file[toml]>=0.12.0,<0.13.0',
 'lirc>=1.0.1,<2.0.0',
 'numpy>=1.20.2,<2.0.0',
 'opencv-python>=4.5.1,<5.0.0',
 'pytesseract>=0.3.7,<0.4.0']

entry_points = \
{'console_scripts': ['stb = stb.cli.runner:stb']}

setup_kwargs = {
    'name': 'stb-automator',
    'version': '0.1.0',
    'description': 'A library for automated control & testing of set-top boxes',
    'long_description': '# Stb Automator\n\n> Automated Control & Testing for Set-Top Boxes\n\n![Python](https://img.shields.io/badge/python-%203.7%20%7C%203.8%20%7C%203.9-blue)\n![Platform](https://img.shields.io/badge/platform-linux-blue)\n[![Version](https://img.shields.io/pypi/v/stb-automator)](https://pypi.org/project/stb-automator/)\n[![Black](https://img.shields.io/badge/style-black-black)](https://pypi.org/project/black/)\n[![Build Status](https://github.com/eugenetriguba/stb-automator/workflows/python%20package%20ci/badge.svg?branch=master)](https://github.com/eugenetriguba/stb-automator/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/eugenetriguba/stb-automator/branch/master/graph/badge.svg)](https://codecov.io/gh/eugenetriguba/stb-automator)\n[![Documentation Status](https://readthedocs.org/projects/stb-automator/badge/?version=latest)](https://stb-automator.readthedocs.io/en/latest/?badge=latest)\n\nStb-automator allows you to issue commands to your set-top box (or whatever device you\'re wanting to control that takes in IR). It can then anaylze the behavior of the device and how it responds to those commands by\ninspecting the video output (using image recognition and OCR).\n\nFull documentation can be found at https://stb-automator.readthedocs.io\n\n## Usage\n\nStb-automator is a regular python library. It does not come with a test runner or enforce a way for you to write your tests. You can use it with python\'s unittest or a third party library like pytest.\n\n```python\nimport stb\n\nfrom pathlib import Path\n\n\n# BaseFrame is a core class to inherit from so we can\n# use the PageObject design pattern in our tests to ensure\n# they\'re kept readable.\nclass Menu(stb.BaseFrame):\n\n    def __init__(self):\n        super().__init__()\n\n    @property\n    def is_visible(self):\n        return (\n            stb.match_image(Path(\'menu-banner.png\')) and\n            stb.match_text(\'Menu Page\')\n        )\n\ndef test_that_menu_key_brings_us_to_the_menu():\n    stb.Remote("lirc-remote").press("KEY_MENU")\n    assert Menu().is_visible\n\ndef test_that_settings_icon_is_in_active_state_in_menu():\n    remote = stb.Remote("lirc-remote")\n    remote.press("KEY_MENU")\n    stb.wait_until_visible(Menu)\n    remote.press_until_match("KEY_RIGHT", Path("settings-icon-active.png"))\n```\n\nWe can then run our tests using, in this example, pytest.\nIf the waiting for match or pressing until a match times out,\nan exception will be thrown and the test will fail. Otherwise,\nit will pass.\n\n## Installation\n\nTo install the python package, we can do so using pip.\n\n```bash\n$ pip install stb-automator\n```\n\n## Installation Enviroment Requirements\n\nStb-automator requires [OpenCV](https://opencv.org/), [LIRC](http://www.lirc.org/), [Gstreamer](https://gstreamer.freedesktop.org/), and [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) to be setup and installed already on the given system in order to work properly.\n\nIf you use Debian or a Debian derivative, there is a installation script for the prerequisites in `tools/prerequisites-install-debian.sh`. You will still have to figure out setup and configure for LIRC and Gstreamer. Further documentation on how to install these prerequisites and set it all up can be found at the full documentation site: https://stb-automator.readthedocs.io\n',
    'author': 'Eugene Triguba',
    'author_email': 'eugenetriguba@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eugenetriguba/stb-automator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
