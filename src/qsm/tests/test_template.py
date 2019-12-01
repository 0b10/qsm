from qsm.vm import update, install, uninstall
from unittest.mock import patch
import re


def test_update_exists():
    assert update is not None, "should exist, but doesn't"

# >>> UPDATE >>>


def test_update_uses_qvm_run():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        update("fedora-template")
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(r"^qvm-run ", _arg), "qvm-run was not used"


def test_update_executes_dnf_update():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        update("fedora-template")
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r"dnf update[\w\W]+-y", _arg), "dnf is not executed"


def test_update_executes_as_root():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        update("fedora-template")
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r" --user root ", _arg), "update was not run as root"


def test_update_excutes_on_correct_target():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        update("fedora-template")
        _arg = mock_check_call.call_args[0][0]

        assert re.search(
            r" fedora-template ", _arg), "update not executed on the correct target"

# >>> INSTALL >>>


def test_install_uses_qvm_run():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        install("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r"^qvm-run ", _arg), "qvm-run was not used"


def test_install_executes_dnf_install():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        install("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r"dnf install -y vim nano", _arg), "dnf is not executed"


def test_install_executes_as_root():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        install("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r" --user root ", _arg), "install was not run as root"


def test_install_excutes_on_correct_target():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        install("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        assert re.search(
            r" fedora-template ", _arg), "install not executed on the correct target"


# >>> UNINSTALL >>>


def test_uninstall_uses_qvm_run():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        uninstall("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r"^qvm-run ", _arg), "qvm-run was not used"


def test_uninstall_executes_dnf_remove():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        uninstall("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r"dnf remove -y vim nano", _arg), "dnf is not executed"


def test_uninstall_executes_as_root():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        uninstall("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r" --user root ", _arg), "uninstall was not run as root"


def test_uninstall_excutes_on_correct_target():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        uninstall("fedora-template", ["vim",  "nano"])
        _arg = mock_check_call.call_args[0][0]

        assert re.search(
            r" fedora-template ", _arg), "uninstall not executed on the correct target"
