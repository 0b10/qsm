# MIT License
#
# Copyright (c) 2019 0b10
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from qsm.remote import update, install, remove
import re


# >>> UPDATE >>>


def test_update_returns_a_string():
    assert isinstance(update(), str), "did not return a string"


def test_update_returns_an_expected_value():
    assert re.search("dnf update -y", update()
                     ), "did not return an update script"

# >>> INSTALL >>>


def test_install_returns_a_string():
    assert isinstance(install("vim nano"), str), "did not return a string"


def test_install_returns_an_expected_value():
    assert re.search("dnf install -y vim", install("vim")
                     ), "did not return an install script"

# >>> REMOVE >>>


def test_remove_returns_a_string():
    assert isinstance(remove("vim nano"), str), "did not return a string"


def test_remove_returns_an_expected_value():
    assert re.search("dnf remove -y vim nano", remove("vim nano")
                     ), "did not return an install script"
