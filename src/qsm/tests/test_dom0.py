from qsm import dom0, lib
from unittest.mock import patch
import pytest
from qsm.constants import QVM_CHECK_DOMAIN_NOT_FOUND


# >>> exists() >>>


def test_exists_return_true_when_vm_exists():
    with patch("qsm.dom0.run", return_value=None, autospec=True):
        assert dom0.exists("fedora-template") is True


def test_exists_return_false_when_vm_doesnt_exist():
    with patch("qsm.dom0.run", side_effect=lib.QsmProcessError(QVM_CHECK_DOMAIN_NOT_FOUND), autospec=True):
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
