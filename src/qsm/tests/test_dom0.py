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

# >>> not_exists_or_throws() >>>


def test_not_exists_or_throws_return_true_when_vm_exists():
    with patch("qsm.dom0.exists", return_value=False, autospec=True):
        assert dom0.not_exists_or_throws("fedora-template") is True


def test_not_exists_or_throws_throws_when_vm_doesnt_exist():
    # returncode 2 is "domain not found"
    with patch("qsm.dom0.exists", return_value=True, autospec=True):
        with pytest.raises(lib.QsmPreconditionError):
            dom0.not_exists_or_throws("fedora-template")


def test_not_exists_or_throws_throws_for_unexpected_exit_code():
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


# >>> create() >>>


def test_create_exists_ok_doesnt_throw_when_vm_exists():
    # run should return None (exit code 0) when vm exists
    with patch("qsm.dom0.run", return_value=None, autospec=True):
        try:
            dom0.create("fedora-template", "red", exists_ok=True)
        except lib.QsmProcessError:
            pytest.fail(
                "create should not throw when vm exists, and exists_ok=True")


def test_create_exists_ok_false_throws_when_vm_exists():
    # run should return None (exit code 0) when vm exists
    with patch("qsm.dom0.run", return_value=None, autospec=True):
        with pytest.raises(lib.QsmPreconditionError):
            dom0.create("fedora-template", "red", exists_ok=False)


def test_create_exists_ok_throws_when_unexpected_exit_code():
    # run should exit(2) when vm doesn't exist, so any exit code other than that
    with patch("qsm.dom0.run", side_effect=lib.QsmProcessError(273863), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.create("fedora-template", "red", exists_ok=True)


# >>> vm_prefs() >>>


def test_vm_prefs_executes_if_vm_exists():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
        # run returns None for successful run
        with patch("qsm.dom0.run", return_value=None, autospec=True) as mock_run:
            dom0.vm_prefs("fedora-template", {"qrexec_timeout": "120"})
            assert mock_run.called, "run was not called, vm_prefs not executed"


def test_vm_prefs_throws_if_vm_doesnt_exist():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmPreconditionError, autospec=True):
        with pytest.raises(lib.QsmPreconditionError):
            dom0.vm_prefs("fedora-template", {"qrexec_timeout": "120"})


# >>> start() >>>


def test_start_executes_if_vm_exists():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
        # run returns None for successful run
        with patch("qsm.dom0.run", return_value=None, autospec=True) as mock_run:
            dom0.start("fedora-template")
            assert mock_run.called, "run was not called, start not executed"


def test_start_throws_if_vm_doesnt_exist():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmPreconditionError, autospec=True):
        with pytest.raises(lib.QsmPreconditionError):
            dom0.start("fedora-template")

# >>> stop() >>>


def test_stop_executes_if_vm_exists_and_running():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
        with patch("qsm.dom0.is_running", return_value=True, autospec=True):
            # run returns None for successful run
            with patch("qsm.dom0.run", return_value=None, autospec=True) as mock_run:
                dom0.stop("fedora-template")
                assert mock_run.called, "run was not called, stop not executed"


def test_stop_executes_if_vm_exists_and_not_running():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
        with patch("qsm.dom0.is_running", return_value=False, autospec=True):
            # run returns None for successful run
            with patch("qsm.dom0.run", return_value=None, autospec=True):
                # qvm-shutdown is never executed if the vm isn't running
                # so the function just completes without failure
                assert dom0.stop("fedora-template") is None


def test_stop_throws_if_vm_doesnt_exist():
    # exists_or_throws throws when vm doesn't exist
    with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmPreconditionError, autospec=True):
        with pytest.raises(lib.QsmPreconditionError):
            dom0.stop("fedora-template")

# >>> clone() >>>


def test_clone_executes_if_vm_exists():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
        # run returns None for successful run
        with patch("qsm.dom0.run", return_value=None, autospec=True) as mock_run:
            dom0.stop("fedora-template")
            assert mock_run.called, "run was not called, stop not executed"


def test_clone_throws_if_vm_doesnt_exist():
    # exists_or_throws throws when vm doesn't exist
    with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmPreconditionError, autospec=True):
        # run returns None for successful run
        with patch("qsm.dom0.run", return_value=None, autospec=True):
            with pytest.raises(lib.QsmPreconditionError):
                dom0.stop("fedora-template")
