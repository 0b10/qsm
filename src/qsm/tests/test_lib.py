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
from qsm.lib import run
from unittest.mock import patch
import re


def test_run_exists():
    assert run is not None

# >>> RUN >>>
# ~~~ DOM0 ~~~


def test_dom0_command_is_executed():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(
            r"ls -l", _arg), "command was not executed in dom0"


def test_dom0_command_is_executed_as_user():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"sudo --user=user",
                         _arg), "dom0 command was not executed as user"


def test_dom0_command_is_executed_as_root():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "root")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"sudo --user=root",
                         _arg), "dom0 command was not executed as root"

# ~~~ DOMU ~~~


def test_domU_command_is_executed():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"^qvm-run[\w\W]+domU",
                         _arg), "command was not executed in domU"


def test_domU_command_is_executed_as_user():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"^qvm-run[\w\W]+--user user",
                         _arg), "domU command not executed as user"


def test_domU_command_is_executed_as_root():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "root")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"^qvm-run[\w\W]+--user root",
                         _arg), "domU command not executed as root"
