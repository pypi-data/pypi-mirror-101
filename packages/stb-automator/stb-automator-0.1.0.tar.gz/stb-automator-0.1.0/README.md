# Stb Automator

> Automated Control & Testing for Set-Top Boxes

![Python](https://img.shields.io/badge/python-%203.7%20%7C%203.8%20%7C%203.9-blue)
![Platform](https://img.shields.io/badge/platform-linux-blue)
[![Version](https://img.shields.io/pypi/v/stb-automator)](https://pypi.org/project/stb-automator/)
[![Black](https://img.shields.io/badge/style-black-black)](https://pypi.org/project/black/)
[![Build Status](https://github.com/eugenetriguba/stb-automator/workflows/python%20package%20ci/badge.svg?branch=master)](https://github.com/eugenetriguba/stb-automator/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/eugenetriguba/stb-automator/branch/master/graph/badge.svg)](https://codecov.io/gh/eugenetriguba/stb-automator)
[![Documentation Status](https://readthedocs.org/projects/stb-automator/badge/?version=latest)](https://stb-automator.readthedocs.io/en/latest/?badge=latest)

Stb-automator allows you to issue commands to your set-top box (or whatever device you're wanting to control that takes in IR). It can then anaylze the behavior of the device and how it responds to those commands by
inspecting the video output (using image recognition and OCR).

Full documentation can be found at https://stb-automator.readthedocs.io

## Usage

Stb-automator is a regular python library. It does not come with a test runner or enforce a way for you to write your tests. You can use it with python's unittest or a third party library like pytest.

```python
import stb

from pathlib import Path


# BaseFrame is a core class to inherit from so we can
# use the PageObject design pattern in our tests to ensure
# they're kept readable.
class Menu(stb.BaseFrame):

    def __init__(self):
        super().__init__()

    @property
    def is_visible(self):
        return (
            stb.match_image(Path('menu-banner.png')) and
            stb.match_text('Menu Page')
        )

def test_that_menu_key_brings_us_to_the_menu():
    stb.Remote("lirc-remote").press("KEY_MENU")
    assert Menu().is_visible

def test_that_settings_icon_is_in_active_state_in_menu():
    remote = stb.Remote("lirc-remote")
    remote.press("KEY_MENU")
    stb.wait_until_visible(Menu)
    remote.press_until_match("KEY_RIGHT", Path("settings-icon-active.png"))
```

We can then run our tests using, in this example, pytest.
If the waiting for match or pressing until a match times out,
an exception will be thrown and the test will fail. Otherwise,
it will pass.

## Installation

To install the python package, we can do so using pip.

```bash
$ pip install stb-automator
```

## Installation Enviroment Requirements

Stb-automator requires [OpenCV](https://opencv.org/), [LIRC](http://www.lirc.org/), [Gstreamer](https://gstreamer.freedesktop.org/), and [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) to be setup and installed already on the given system in order to work properly.

If you use Debian or a Debian derivative, there is a installation script for the prerequisites in `tools/prerequisites-install-debian.sh`. You will still have to figure out setup and configure for LIRC and Gstreamer. Further documentation on how to install these prerequisites and set it all up can be found at the full documentation site: https://stb-automator.readthedocs.io
