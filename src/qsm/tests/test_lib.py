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
import faker
import hypothesis.strategies as s
from faker import providers


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
def test__is_ipv4__happy_path():
    fake = faker.Faker()
    fake.add_provider(providers.internet)
    for _ in range(50):
        ip = fake.ipv4(network=False)
        assert lib.is_ipv4(ip), \
            "should return True for {}".format(ip)


@hypothesis.given(s.text())
def test__is_ipv4__fuzz_random_string(random_string):
    assert not lib.is_ipv4(random_string), \
        "should return False for {}".format(random_string)


def test__is_ipv4_network__happy_path():
    fake = faker.Faker()
    fake.add_provider(providers.internet)
    for _ in range(50):
        ip = fake.ipv4(network=True)
        assert lib.is_ipv4_network(ip), \
            "should return True for {}".format(ip)


@hypothesis.given(s.text())
def test__is_ipv4_network__fuzz_random_string(random_string):
    assert not lib.is_ipv4_network(random_string), \
        "should return False for {}".format(random_string)


# ~~~ is_ipv6() ~~~
def test__is_ipv6__happy_path():
    fake = faker.Faker()
    fake.add_provider(providers.internet)
    for _ in range(50):
        ip = fake.ipv6(network=False)
        assert lib.is_ipv6(ip), \
            "should return True for {}".format(ip)


@hypothesis.given(s.text())
def test__is_ipv6__fuzz_random_string(random_string):
    assert not lib.is_ipv6(random_string), \
        "should return False for {}".format(random_string)


def test__is_ipv6_network__happy_path():
    fake = faker.Faker()
    fake.add_provider(providers.internet)
    for _ in range(50):
        ip = fake.ipv6(network=True)
        assert lib.is_ipv6_network(ip), \
            "should return True for {}".format(ip)


@hypothesis.given(s.text())
def test__is_ipv6_network__fuzz_random_string(random_string):
    assert not lib.is_ipv6_network(random_string), \
        "should return False for {}".format(random_string)


# ~~~ is_meaningful_string() ~~~

def test_is_meaningful_string_rejects_empty_string():
    assert not lib.is_meaningful_string(
        ""), "an empty string should be rejected"


def test_is_meaningful_string_happy_path_fuzz():
    assert lib.is_meaningful_string("text"), "should be accepted"


# ~~~ is_mac() ~~~

def test_is_mac_accepts_mac():
    assert lib.is_mac("00:01:36:12:e6:ff"), "should accept a mac address"


@hypothesis.given(s.text())
def test_is_mac_rejects_non_mac(text):
    assert not lib.is_mac(text), "should reject non-macs"
