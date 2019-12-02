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
from qsm import vm
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
@hypothesis.given(s.booleans())
def test_vm_prefs_builder_bools_happy_fuzz(value):
    _prefs = vm.VmPrefsBuilder()
    _methods = [_prefs.autostart, _prefs.debug, _prefs.include_in_backups,
                _prefs.provides_network, _prefs.template_for_dispvms]

    for _method in _methods:
        assert _method(value), "should accept a boolean"


@hypothesis.given(s.one_of(s.text(), s.complex_numbers(), s.decimals()))
def test_vm_prefs_builder_bools_negative_fuzz(value):
    _prefs = vm.VmPrefsBuilder()
    _methods = [_prefs.autostart, _prefs.debug, _prefs.include_in_backups,
                _prefs.provides_network, _prefs.template_for_dispvms]

    for _method in _methods:
        with pytest.raises(AssertionError):
            _method(value)
