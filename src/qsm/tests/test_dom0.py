from qsm import dom0, lib
from unittest.mock import patch
import pytest
from qsm.constants import QVM_CHECK_EXISTS_NOT_FOUND, QVM_CHECK_IS_NOT_RUNNING


# >>> exists() >>>


def test_exists_returns_true_when_vm_exists():
    with patch("qsm.dom0.run", return_value=None, autospec=True):
        assert dom0.exists("fedora-template") is True


def test_exists_returns_false_when_vm_doesnt_exist():
    with patch("qsm.dom0.run", side_effect=lib.QsmProcessError(QVM_CHECK_EXISTS_NOT_FOUND), autospec=True):
        assert dom0.exists("fedora-template") is False


def test_exists_throws_for_unexpected_exit_code():
    # returncode 2 is "domain not found"
    with patch("qsm.dom0.run", side_effect=lib.QsmProcessError(237687263), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.exists("fedora-template")

# >>> exists_or_throws() >>>


def test_exists_or_throws_return_true_when_vm_exists():
    with patch("qsm.dom0.exists", return_value=True, autospec=True):
        assert dom0.exists_or_throws("fedora-template") is True


def test_exists_or_throws_throws_when_vm_doesnt_exist():
    # returncode 2 is "domain not found"
    with patch("qsm.dom0.exists", return_value=False, autospec=True):
        with pytest.raises(lib.QsmPreconditionError):
            dom0.exists_or_throws("fedora-template")


def test_exists_or_throws_throws_for_unexpected_exit_code():
    # returncode 2 is "domain not found"
    with patch("qsm.dom0.run", side_effect=lib.QsmProcessError(237687263), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.exists("fedora-template")


# >>> is_running() >>>


def test_is_running_returns_true_when_vm_is_running():
    # returncode 0 for a running vm, so run doesn't throw
    with patch("qsm.dom0.run", return_value=None, autospec=True):
        assert dom0.is_running("fedora-template") is True


def test_is_running_returns_false_when_vm_isnt_running():
    with patch("qsm.dom0.run", side_effect=lib.QsmProcessError(QVM_CHECK_IS_NOT_RUNNING), autospec=True):
        assert dom0.is_running("fedora-template") is False


def test_is_running_throws_for_unexpected_exit_code():
    # returncode 1 is "domain is running"
    with patch("qsm.dom0.run", side_effect=lib.QsmProcessError(7612736), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.is_running("fedora-template")

# >>> is_running_or_throws() >>>


def test_is_running_or_throws_returns_true_when_vm_is_running():
    # returncode 0 for a running vm, so run doesn't throw
    with patch("qsm.dom0.is_running", return_value=True, autospec=True):
        assert dom0.is_running_or_throws("fedora-template") is True


def test_is_running_or_throws_throws_when_vm_isnt_running():
    with patch("qsm.dom0.is_running", return_value=False, autospec=True):
        with pytest.raises(lib.QsmPreconditionError):
            assert dom0.is_running_or_throws("fedora-template")


def test_is_running_or_throws_throws_for_unexpected_exit_code():
    # returncode 1 is "domain is running"
    with patch("qsm.dom0.run", side_effect=lib.QsmProcessError(7612736), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.is_running_or_throws("fedora-template")


# >>> is_stopped_or_throws() >>>


def test_is_stopped_or_throws_returns_true_when_vm_is_not_running():
    # returncode 0 for a running vm, so run doesn't throw
    with patch("qsm.dom0.is_running", return_value=False, autospec=True):
        assert dom0.is_stopped_or_throws("fedora-template") is True


def test_is_stopped_or_throws_throws_when_vm_is_running():
    with patch("qsm.dom0.is_running", return_value=True, autospec=True):
        with pytest.raises(lib.QsmPreconditionError):
            assert dom0.is_stopped_or_throws("fedora-template")


def test_is_stopped_or_throws_throws_for_unexpected_exit_code():
    # returncode 1 is "domain is running"
    with patch("qsm.dom0.run", side_effect=lib.QsmProcessError(7612736), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.is_stopped_or_throws("fedora-template")
