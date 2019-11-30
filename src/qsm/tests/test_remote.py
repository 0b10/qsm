import pytest
from qsm.remote import get
from unittest.mock import patch
import re


def test_get_exists():
    assert get != None, "does not exist"

# >>> ERROR >>>


def test_get_accepts_valid_target():
    try:
        get("update")
    except:
        pytest.fail("shouldn't throw, but did")


def test_get_rejects_invalid_target():
    with pytest.raises(AssertionError):
        get("jahdslkjhd")

# >>> UPDATE >>>


def test_get_update_return_string():
    assert isinstance(get("update"), str), "did not return a string"


def test_get_update_return_expected_value():
    assert re.search("dnf update -y", get("update")
                     ), "did not return an update script"
