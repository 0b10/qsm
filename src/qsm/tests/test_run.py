import pytest
from qsm.run import run, run_remote
from unittest.mock import patch
import re


def test_run_exists():
    assert run != None

# >>> DOM0 >>>


def test_dom0_command_is_executed():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user", "bash")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(
            "bash -c ls -l", _arg), "command was not executed in dom0"


def test_dom0_command_executes_bash():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user", "bash")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(
            "bash -c ls -l", _arg), "bash was not executed in dom0"


def test_dom0_command_executes_zsh():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user", "zsh")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("zsh -c ls -l", _arg), "zsh was not executed in dom0"


def test_dom0_command_executes_python():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("script.py", "dom0", "user", "python")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("python script.py",
                         _arg), "python was not executed in dom0"


def test_dom0_command_is_executed_as_user():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user", "bash")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("sudo --user=user",
                         _arg), "dom0 command was not executed as user"


def test_dom0_command_is_executed_as_root():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "root", "bash")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("sudo --user=root",
                         _arg), "dom0 command was not executed as root"

# >>> DOMU >>>


def test_domU_command_is_executed():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user", "bash")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("^qvm-run[\w\W]+domU",
                         _arg), "command was not executed in domU"


def test_domU_command_executes_bash():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user", "bash")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("^qvm-run[\w\W]+bash -c ls -l",
                         _arg), "bash was not executed in odmu"


def test_domU_command_executes_zsh():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user", "zsh")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("^qvm-run[\w\W]+zsh -c ls -l",
                         _arg), "zsh was not executed in domU"


def test_domU_command_executes_python():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("script.py", "domU", "user", "python")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("^qvm-run[\w\W]+python script.py",
                         _arg), "python was not executed in domU"


def test_domU_command_is_executed_as_user():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user", "bash")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("^qvm-run[\w\W]+--user user",
                         _arg), "domU command not executed as user"


def test_domU_command_is_executed_as_root():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "root", "bash")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("^qvm-run[\w\W]+--user root",
                         _arg), "domU command not executed as root"

# >>> run_remote >>>


def test_run_remote_executes_python():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run_remote("a = 1", "domU", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("^qvm-run[\w\W]+python3 -c \'a = 1\'",
                         _arg), "python inline script was not executed in domU"


def test_run_remote_executes_python_as_root():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run_remote("a = 1", "domU", "root")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("^qvm-run[\w\W]+--user root",
                         _arg), "python inline script was not executed as root"


def test_run_remote_executes_python_as_user():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run_remote("a = 1", "domU", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("^qvm-run[\w\W]+--user user",
                         _arg), "python inline script was not executed as user"

def test_run_remote_targets_given_domU():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run_remote("a = 1", "domU", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search("^qvm-run[\w\W]+domU",
                         _arg), "python inline script was not executed as user"


def test_run_remote_executes_script_with_args():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        run_remote("a = 1", "domU", "user", ["some string", "argB"])
        _arg = mock_check_call.call_args[0][0]
        assert re.search("^qvm-run[\w\W]+\'some string\' \'argB\'",
                         _arg), "python inline script did not receive args"
