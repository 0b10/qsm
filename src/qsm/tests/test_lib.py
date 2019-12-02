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
from qsm import lib
from unittest.mock import patch
import re
import hypothesis
import hypothesis.strategies as s


def test_run_exists():
    assert lib.run is not None

# >>> RUN >>>
# ~~~ DOM0 ~~~


def test_dom0_command_is_executed():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        lib.run("ls -l", "dom0", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(
            r"ls -l", _arg), "command was not executed in dom0"


def test_dom0_command_is_executed_as_user():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        lib.run("ls -l", "dom0", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"sudo --user=user",
                         _arg), "dom0 command was not executed as user"


def test_dom0_command_is_executed_as_root():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        lib.run("ls -l", "dom0", "root")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"sudo --user=root",
                         _arg), "dom0 command was not executed as root"

# ~~~ DOMU ~~~


def test_domU_command_is_executed():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        lib.run("ls -l", "domU", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"^qvm-run[\w\W]+domU",
                         _arg), "command was not executed in domU"


def test_domU_command_is_executed_as_user():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        lib.run("ls -l", "domU", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"^qvm-run[\w\W]+--user user",
                         _arg), "domU command not executed as user"


def test_domU_command_is_executed_as_root():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        lib.run("ls -l", "domU", "root")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"^qvm-run[\w\W]+--user root",
                         _arg), "domU command not executed as root"


# >>> PREDICATES >>>
# ~~~ is_ipv4() ~~~

def test_is_ipv4_happy_path():
    for num in range(0, 255):
        assert lib.is_ipv4("{0}.{0}.{0}.{0}".format(num)), \
            "{0}.{0}.{0}.{0} should be accepted".format(num)


def test_is_ipv4_happy_boundaries():
    for num in range(256, 300):
        assert not lib.is_ipv4("{0}.{0}.{0}.{0}".format(num)), \
            "{0}.{0}.{0}.{0} should be accepted".format(num)

    for num in range(-50, -1):
        assert not lib.is_ipv4("{0}.{0}.{0}.{0}".format(num)), \
            "{0}.{0}.{0}.{0} should be accepted".format(num)


@hypothesis.given(s.text())
def test_is_ipv4_random_string(random_string):
    assert not lib.is_ipv4(random_string), \
        "{} should be rejected".format(random_string)

# ~~~ is_meaningful_string() ~~~


def test_is_meaningful_string_rejects_empty_string():
    assert not lib.is_meaningful_string(""), "an empty string should be rejected"


def test_is_meaningful_string_happy_path_fuzz():
    assert lib.is_meaningful_string("text"), "should be accepted"


# ~~~ is_uuid() ~~~


@hypothesis.given(s.uuids())
def test_is_uuid_happy_path_fuzz(uuid):
    assert lib.is_uuid(str(uuid)), "should be accepted: {}".format(uuid)


@hypothesis.given(s.text())
def test_is_uuid_negative_path_fuzz(text):
    assert not lib.is_uuid(text), "should be rejected: {}".format(text)
