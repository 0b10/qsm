from qsm.remote import update, install
import re


# >>> UPDATE >>>


def test_update_returns_a_string():
    assert isinstance(update(), str), "did not return a string"


def test_update_returns_an_expected_value():
    assert re.search("dnf update -y", update()
                     ), "did not return an update script"


# >>> INSTALL >>>

def test_install_returns_a_string():
    assert isinstance(install("vim nano"), str), "did not return a string"


def test_install_returns_an_expected_value():
    assert re.search("dnf install -y", install()
                     ), "did not return an install script"
