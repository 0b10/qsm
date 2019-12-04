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
import pytest
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
# ~~~ is_ip() ~~~
def test__is_ip__happy_path():
    """Test that any valid ipv4/v6 address will return True for network addresses when network=True"""
    fake = faker.Faker()
    fake.add_provider(providers.internet)
    test_cases = [
        fake.ipv4(network=False),
        fake.ipv4(network=True),
        fake.ipv6(network=False),
        fake.ipv6(network=True),
    ]

    for ip in test_cases:
        assert lib.is_ip(ip, network=True), \
            "should return True for {}".format(ip)


def test__is_ip__network_true__happy_path():
    """Test that any valid ipv4/v6 address will return True for non-network addresses when network=False"""
    fake = faker.Faker()
    fake.add_provider(providers.internet)
    test_cases = [
        fake.ipv4(network=False),
        fake.ipv6(network=False),
    ]

    for ip in test_cases:
        assert lib.is_ip(ip, network=False), \
            "should return True for {}".format(ip)


def test__is_ip__not_net__negative():
    """Test that a network ip will cause False to be returned, when network=False"""
    fake = faker.Faker()
    fake.add_provider(providers.internet)
    test_cases = [
        fake.ipv4(network=True),
        fake.ipv6(network=True),
    ]

    for ip in test_cases:
        assert not lib.is_ip(ip, network=False), \
            "should return False for {}".format(ip)


@pytest.mark.parametrize("value", [
    "1",
    "1,2",
    "1-2",
    "1-2,3",
    "4,1-2,3",
    "65535",
    "65534-65535",
    "2000,65534-65535",
])
def test__assert_valid_dstports__happy_path(value):
    assert lib.assert_valid_dstports(value), \
        "{} should return True".format(value)


@pytest.mark.parametrize("value", [
    "1 ",
    "1+2",
    "65536",
    "100000",
    "0",
    "-",
    "-0",
    "1-0",
    "1--1",
    "-1",
])
def test__assert_valid_dstports__negative(value):
    with pytest.raises(AssertionError):
        lib.assert_valid_dstports(value)


_valid_ports_strat = s.integers(min_value=1, max_value=65535)
@hypothesis.given(_valid_ports_strat, _valid_ports_strat, _valid_ports_strat)
def test__assert_valid_dstports__happy_fuzz(one, two, three):
    """Test a range of valid ports, in various configurations"""
    cases = [
        str(one),
        "{},{}".format(one, two),
        "{},{}-{}".format(one, two, three),
        "{0},{1}-{2},{0}".format(one, two, three),
        "{0},{1}-{2},{0}-{2},{0}".format(one, two, three)
    ]

    for case in cases:
        assert lib.assert_valid_dstports(str(case)), \
            "{} should return True".format(case)


_invalid_ports_strat_1 = s.integers(min_value=65536, max_value=100000)
_invalid_ports_strat_2 = s.integers(min_value=-100000, max_value=0)
@hypothesis.given(_invalid_ports_strat_1, _invalid_ports_strat_2, _invalid_ports_strat_1)
def test__assert_valid_dstports__negative_fuzz(one, two, three):
    """Test a range of valid ports, in various configurations"""
    cases = [
        str(one),
        "{},{}".format(one, two),
        "{},{}-{}".format(one, two, three),
        "{0},{1}-{2},{0}".format(one, two, three),
        "{0},{1}-{2},{0}-{2},{0}".format(one, two, three)
    ]

    for case in cases:
        with pytest.raises(AssertionError):
            lib.assert_valid_dstports(str(case))


@hypothesis.given(s.text())
def test__is_ip__fuzz_random_string(random_string):
    assert not lib.is_ip(random_string), \
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
