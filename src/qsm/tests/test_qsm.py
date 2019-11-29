import pytest
import qsm


def test_project_defines_author_and_version():
    assert hasattr(qsm, '__author__')
    assert hasattr(qsm, '__version__')
