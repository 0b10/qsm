from qsm.template import update, install
from unittest.mock import patch
import re


def test_update_exists():
    assert update is not None, "should exist, but doesn't"


def test_update_executes_update_script():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        update("fedora-template")
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r"^qvm-run --user root[\w\W]+fedora-template[\w\W]+dnf update -y[\w\W]+$", _arg), \
            "qvm-run as root, and/or update script not executed"


def test_install_executes_install_script():
    with patch("qsm.run.check_call", return_value=0, autospec=True) as mock_check_call:
        install("fedora-template", ["vim nano", "another_arg"])
        _arg = mock_check_call.call_args[0][0]

        # \w\W any char including newline
        assert re.search(
            r"^qvm-run --user root[\w\W]+fedora-template[\w\W]+dnf install -y[\w\W]+\'vim nano\' \'another_arg\'", _arg), \
            "qvm-run as root, and/or install script not executed properly"
