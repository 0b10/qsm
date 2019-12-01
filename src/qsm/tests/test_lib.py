from qsm.lib import run
from unittest.mock import patch
import re


def test_run_exists():
    assert run is not None

# >>> RUN >>>
# ~~~ DOM0 ~~~


def test_dom0_command_is_executed():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(
            r"ls -l", _arg), "command was not executed in dom0"


def test_dom0_command_is_executed_as_user():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"sudo --user=user",
                         _arg), "dom0 command was not executed as user"


def test_dom0_command_is_executed_as_root():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "dom0", "root")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"sudo --user=root",
                         _arg), "dom0 command was not executed as root"

# ~~~ DOMU ~~~


def test_domU_command_is_executed():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"^qvm-run[\w\W]+domU",
                         _arg), "command was not executed in domU"


def test_domU_command_is_executed_as_user():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "user")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"^qvm-run[\w\W]+--user user",
                         _arg), "domU command not executed as user"


def test_domU_command_is_executed_as_root():
    with patch("qsm.lib.check_call", return_value=0, autospec=True) as mock_check_call:
        run("ls -l", "domU", "root")
        _arg = mock_check_call.call_args[0][0]
        assert re.search(r"^qvm-run[\w\W]+--user root",
                         _arg), "domU command not executed as root"
