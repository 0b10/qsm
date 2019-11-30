import pytest
from qsm.run import run
from unittest.mock import patch


def test_run_exists():
    assert run != None

# >>> DOM0 >>>


def test_dom0_command_is_executed():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user", "bash")
        mock_check_call.assert_called_once_with(
            "sudo --user=user bash -c ls -l", shell=True)


def test_dom0_command_executes_bash():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user", "bash")
        mock_check_call.assert_called_once_with(
            "sudo --user=user bash -c ls -l", shell=True)


def test_dom0_command_executes_zsh():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user", "zsh")
        mock_check_call.assert_called_once_with(
            "sudo --user=user zsh -c ls -l", shell=True)


def test_dom0_command_executes_python():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user", "python")
        mock_check_call.assert_called_once_with(
            "sudo --user=user python ls -l", shell=True)


def test_dom0_command_is_executed_as_user():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user", "bash")
        mock_check_call.assert_called_once_with(
            "sudo --user=user bash -c ls -l", shell=True)


def test_dom0_command_is_executed_as_root():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "root", "bash")
        mock_check_call.assert_called_once_with(
            "sudo --user=root bash -c ls -l", shell=True)

# >>> DOMU >>>


def test_domU_command_is_executed():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user", "bash")
        mock_check_call.assert_called_once_with(
            'qvm-run --user user --pass-io domU "bash -c ls -l"', shell=True)


def test_domU_command_executes_bash():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user", "bash")
        mock_check_call.assert_called_once_with(
            'qvm-run --user user --pass-io domU "bash -c ls -l"', shell=True)


def test_domU_command_executes_zsh():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user", "zsh")
        mock_check_call.assert_called_once_with(
            'qvm-run --user user --pass-io domU "zsh -c ls -l"', shell=True)


def test_domU_command_executes_python():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user", "python")
        mock_check_call.assert_called_once_with(
            'qvm-run --user user --pass-io domU "python ls -l"', shell=True)


def test_domU_command_is_executed_as_user():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user", "bash")
        mock_check_call.assert_called_once_with(
            'qvm-run --user user --pass-io domU "bash -c ls -l"', shell=True)


def test_domU_command_is_executed_as_root():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "root", "bash")
        mock_check_call.assert_called_once_with(
            'qvm-run --user root --pass-io domU "bash -c ls -l"', shell=True)
