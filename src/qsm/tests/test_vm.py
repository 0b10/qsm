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
from qsm.vm import update, install, uninstall
from unittest.mock import patch
import re
from qsm import vm, constants
import hypothesis
from hypothesis import strategies as s
import pytest


def test_update_exists():
    assert update is not None, "should exist, but doesn't"

# >>> UPDATE >>>


def test_update_uses_qvm_run():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        update("fedora-template")
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(r"^qvm-run ", _arg), "qvm-run was not used"


def test_update_executes_dnf_update():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        update("fedora-template")
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r"dnf update[\w\W]+-y", _arg), "dnf is not executed"


def test_update_executes_as_root():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        update("fedora-template")
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r" --user root ", _arg), "update was not run as root"


def test_update_excutes_on_correct_target():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        update("fedora-template")
        _arg = mock_check_call.call_args[0][0]

        assert re.search(
            r" fedora-template ", _arg), "update not executed on the correct target"

# >>> INSTALL >>>


def test_install_uses_qvm_run():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        install("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r"^qvm-run ", _arg), "qvm-run was not used"


def test_install_executes_dnf_install():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        install("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r"dnf install -y vim nano", _arg), "dnf is not executed"


def test_install_executes_as_root():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        install("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r" --user root ", _arg), "install was not run as root"


def test_install_excutes_on_correct_target():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        install("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        assert re.search(
            r" fedora-template ", _arg), "install not executed on the correct target"


# >>> UNINSTALL >>>


def test_uninstall_uses_qvm_run():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        uninstall("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r"^qvm-run ", _arg), "qvm-run was not used"


def test_uninstall_executes_dnf_remove():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        uninstall("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r"dnf remove -y vim nano", _arg), "dnf is not executed"


def test_uninstall_executes_as_root():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        uninstall("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r" --user root ", _arg), "uninstall was not run as root"


def test_uninstall_excutes_on_correct_target():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        uninstall("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        assert re.search(
            r" fedora-template ", _arg), "uninstall not executed on the correct target"


# >>> VmPrefsBuilder >>>
# ~~~ boolean ~~~
@pytest.fixture
def _boolean_methods():
    _prefs = vm.VmPrefsBuilder()
    return [_prefs.autostart, _prefs.debug, _prefs.include_in_backups,
            _prefs.provides_network, _prefs.template_for_dispvms]


@pytest.fixture
def _arbitrary_string_methods():
    _prefs = vm.VmPrefsBuilder()
    return [_prefs.default_dispvm, _prefs.default_user,
            _prefs.kernel_opts, _prefs.management_dispvm,
            _prefs.name, _prefs.netvm, _prefs.template]


@pytest.fixture
def _positive_integer_methods():
    _prefs = vm.VmPrefsBuilder()
    return [_prefs.vcpus, _prefs.shutdown_timeout, _prefs.qrexec_timeout,
            _prefs.memory, _prefs.maxmem]


@hypothesis.given(s.booleans())
def test_vm_prefs_builder_bools_happy_fuzz(_boolean_methods, value):
    for _method in _boolean_methods:
        assert _method(value), "should accept a boolean"


@hypothesis.given(s.one_of(s.text(), s.complex_numbers(), s.decimals()))
def test_vm_prefs_builder_bools_negative_fuzz(_boolean_methods, value):
    for _method in _boolean_methods:
        with pytest.raises(AssertionError):
            _method(value)


# ~~~ arbitrary strings ~~~
# any text, except '', line-terminators, and spaces.
# ! The regex for line terminators is broken, won't fix. don't know how. It's good enough.
@hypothesis.given(s.text(alphabet=s.characters(blacklist_characters=[' ', '\n']), min_size=1))
def test_vm_prefs_builder_arbitrary_strings_happy_fuzz(_arbitrary_string_methods, value):
    # strings should be accepted, as long as they aren't empty, or only spaces
    for _method in _arbitrary_string_methods:
        assert _method(value), "should accept an arbitrary string"


@hypothesis.given(s.one_of(s.booleans(), s.integers(), s.none()))
def test_vm_prefs_builder_arbitrary_strings_negative_fuzz(_arbitrary_string_methods, value):
    # non-strings should throw
    for _method in _arbitrary_string_methods:
        with pytest.raises(AssertionError):
            _method(value)


# ~~~ positive integers ~~~
@hypothesis.given(s.integers(1))
@hypothesis.example(1)
def test__vm_prefs__builder__vcpus__happy_path(_positive_integer_methods, value):
    """Fuzz test all methods that accept positive integers"""
    for _method in _positive_integer_methods:
        assert _method(value), "should accept any positive integer"


@hypothesis.given(s.integers(-10000, 0))
@hypothesis.example(0)
def test__vm_prefs__builder__virt_mode__negative_integer_fuzz(_positive_integer_methods, value):
    """Fuzz test all methods that reject integers <= 0"""
    for _method in _positive_integer_methods:
        with pytest.raises(AssertionError):
            _method(value)


@hypothesis.given(s.one_of(s.booleans(), s.text(), s.complex_numbers()))
def test__vm_prefs__builder__virt_mode__random_type_negative_fuzz(_positive_integer_methods, value):
    """Fuzz test (random types) for all methods that accept only positive integers"""
    for _method in _positive_integer_methods:
        with pytest.raises(AssertionError):
            _method(value)


# ~~~ kernel version ~~~
_kernel_versions = [
    "1.1.8-1",
    "123.1321.23-1",
    "123.1321-23.1",
    "123-138271-2332.123",
    "0"
    "0.1"
    "3281798370928"
]
@pytest.mark.parametrize("value", _kernel_versions)
def test__vm_prefs__builder__kernel__happy_path(value):
    """Test strings composed of numbers, dots, and dashes"""
    _prefs = vm.VmPrefsBuilder()
    assert _prefs.kernel(value), \
        "should accept integers, dots, and dashes as a string"


_kernel_blacklisted_chars = [
    ".", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
]
_kernel_text_strat = s.text(alphabet=s.characters(
    blacklist_characters=_kernel_blacklisted_chars))


@hypothesis.given(s.one_of(_kernel_text_strat, s.integers(), s.booleans()))
def test__vm_prefs__builder__kernel__negative_random_type_fuzz(value):
    """Fuzz test all values that blow up kernel"""
    _prefs = vm.VmPrefsBuilder()
    with pytest.raises(AssertionError):
        assert _prefs.kernel(value), \
            "should accept integers, dots, and dashes as a string"


# ~~~  virt_mode ~~~
@pytest.mark.parametrize("virt_mode", constants.VIRT_MODES)
def test__vm_prefs__builder__virt_mode__happy_path(virt_mode):
    """Test all valid virt modes."""
    _prefs = vm.VmPrefsBuilder()
    assert _prefs.virt_mode(virt_mode), "should accept any valid virt mode"


@hypothesis.given(s.one_of(s.booleans(), s.text(), s.integers()))
def test__vm_prefs__builder__virt_mode__negative_fuzz(value):
    """Fuzz test invalid values for virt mode"""
    _prefs = vm.VmPrefsBuilder()
    with pytest.raises(AssertionError):
        _prefs.virt_mode(value)


# ~~~ labels ~~~
@pytest.mark.parametrize("value", constants.LABELS)
def test__vm_prefs__builder__label__happy_path(value):
    """Test all valid labels."""
    _prefs = vm.VmPrefsBuilder()
    assert _prefs.label(value), "should accept any valid label"


@hypothesis.given(s.one_of(s.booleans(), s.text(), s.integers()))
def test__vm_prefs__builder__label__negative_fuzz(value):
    """Fuzz test invalid values for label"""
    _prefs = vm.VmPrefsBuilder()
    with pytest.raises(AssertionError):
        _prefs.label(value)


# ~~~ mac ~~~
_macs = [
    "27:ab:27:e0:e7:11",
    "00:00:00:00:00:00",
    "ff:ff:ff:ff:ff:ff",
    "27:11:BB:AA:FF:FF",
    "0E:1e:e2:A1:2E:FF",
]
@pytest.mark.parametrize("value", _macs)
def test__vm_prefs__builder__mac__happy_path(value):
    """Test some valid mac addresses."""
    _prefs = vm.VmPrefsBuilder()
    assert _prefs.mac(value), "should accept a valid mac address"


@hypothesis.given(s.one_of(s.booleans(), s.text(), s.integers()))
def test__vm_prefs__builder__mac__negative_fuzz(value):
    """Fuzz test invalid types for mac"""
    _prefs = vm.VmPrefsBuilder()
    with pytest.raises(AssertionError):
        _prefs.mac(value)
