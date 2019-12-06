# MIT License

# Copyright (c) 2019 0b10

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from qsm import dom0, lib
from unittest.mock import patch, MagicMock
import pytest
from qsm.constants import QVM_CHECK_EXISTS_NOT_FOUND, QVM_CHECK_IS_NOT_RUNNING
import re
import hypothesis
from hypothesis import strategies as s


# >>> exists() >>>


def test_exists_returns_true_when_vm_exists():
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        assert dom0.exists("fedora-template") is True


def test_exists_returns_false_when_vm_doesnt_exist():
    with patch("qsm.dom0.lib.run", side_effect=lib.QsmProcessError(QVM_CHECK_EXISTS_NOT_FOUND), autospec=True):
        assert dom0.exists("fedora-template") is False


def test_exists_throws_for_unexpected_exit_code():
    # returncode 2 is "domain not found"
    with patch("qsm.dom0.lib.run", side_effect=lib.QsmProcessError(237687263), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.exists("fedora-template")

# >>> exists_or_throws() >>>


def test_exists_or_throws_return_true_when_vm_exists():
    with patch("qsm.dom0.exists", return_value=True, autospec=True):
        assert dom0.exists_or_throws("fedora-template") is True


def test_exists_or_throws_throws_when_vm_doesnt_exist():
    # returncode 2 is "domain not found"
    with patch("qsm.dom0.exists", return_value=False, autospec=True):
        with pytest.raises(lib.QsmDomainDoesntExistError):
            dom0.exists_or_throws("fedora-template")


def test_exists_or_throws_throws_for_unexpected_exit_code():
    # returncode 2 is "domain not found"
    with patch("qsm.dom0.lib.run", side_effect=lib.QsmProcessError(237687263), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.exists("fedora-template")

# >>> not_exists_or_throws() >>>


def test_not_exists_or_throws_return_true_when_vm_exists():
    with patch("qsm.dom0.exists", return_value=False, autospec=True):
        assert dom0.not_exists_or_throws("fedora-template") is True


def test_not_exists_or_throws_throws_when_vm_doesnt_exist():
    # returncode 2 is "domain not found"
    with patch("qsm.dom0.exists", return_value=True, autospec=True):
        with pytest.raises(lib.QsmDomainAlreadyExistError):
            dom0.not_exists_or_throws("fedora-template")


def test_not_exists_or_throws_throws_for_unexpected_exit_code():
    # returncode 2 is "domain not found"
    with patch("qsm.dom0.lib.run", side_effect=lib.QsmProcessError(237687263), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.exists("fedora-template")


# >>> is_running() >>>


def test_is_running_returns_true_when_vm_is_running():
    # returncode 0 for a running vm, so run doesn't throw
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        assert dom0.is_running("fedora-template") is True


def test_is_running_returns_false_when_vm_isnt_running():
    with patch("qsm.dom0.lib.run", side_effect=lib.QsmProcessError(QVM_CHECK_IS_NOT_RUNNING), autospec=True):
        assert dom0.is_running("fedora-template") is False


def test_is_running_throws_for_unexpected_exit_code():
    # returncode 1 is "domain is running"
    with patch("qsm.dom0.lib.run", side_effect=lib.QsmProcessError(7612736), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.is_running("fedora-template")

# >>> is_running_or_throws() >>>


def test_is_running_or_throws_returns_true_when_vm_is_running():
    # returncode 0 for a running vm, so run doesn't throw
    with patch("qsm.dom0.is_running", return_value=True, autospec=True):
        assert dom0.is_running_or_throws("fedora-template") is True


def test_is_running_or_throws_throws_when_vm_isnt_running():
    with patch("qsm.dom0.is_running", return_value=False, autospec=True):
        with pytest.raises(lib.QsmDomainStoppedError):
            assert dom0.is_running_or_throws("fedora-template")


def test_is_running_or_throws_throws_for_unexpected_exit_code():
    # returncode 1 is "domain is running"
    with patch("qsm.dom0.lib.run", side_effect=lib.QsmProcessError(7612736), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.is_running_or_throws("fedora-template")


# >>> is_stopped_or_throws() >>>


def test_is_stopped_or_throws_returns_true_when_vm_is_not_running():
    # returncode 0 for a running vm, so run doesn't throw
    with patch("qsm.dom0.is_running", return_value=False, autospec=True):
        assert dom0.is_stopped_or_throws("fedora-template") is True


def test_is_stopped_or_throws_throws_when_vm_is_running():
    with patch("qsm.dom0.is_running", return_value=True, autospec=True):
        with pytest.raises(lib.QsmDomainRunningError):
            assert dom0.is_stopped_or_throws("fedora-template")


def test_is_stopped_or_throws_throws_for_unexpected_exit_code():
    # returncode 1 is "domain is running"
    with patch("qsm.dom0.lib.run", side_effect=lib.QsmProcessError(7612736), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.is_stopped_or_throws("fedora-template")


# >>> create() >>>


def test_create_exists_ok_doesnt_throw_when_vm_exists():
    # run should return None (exit code 0) when vm exists
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True) as mock_run:
        try:
            dom0.create("fedora-template", "red", exists_ok=True)
        except lib.QsmProcessError:
            pytest.fail(
                "create should not throw when vm exists, and exists_ok=True")

        assert mock_run.called, "run was not called, vm not created"


def test_create_exists_ok_false_throws_when_vm_exists():
    # run should return None (exit code 0) when vm exists
    with patch("qsm.dom0.not_exists_or_throws", side_effect=lib.QsmDomainAlreadyExistError, autospec=True):
        with pytest.raises(lib.QsmDomainAlreadyExistError):
            dom0.create("fedora-template", "red", exists_ok=False)


def test_create_exists_ok_false_creates_a_vm():
    # run should return None (exit code 0) when vm exists
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.not_exists_or_throws", return_value=True, autospec=True) as mock_exists:
            dom0.create("fedora-template", "red", exists_ok=False)
            assert mock_exists.called, "run was not called, vm not created"


def test_create_exists_ok_throws_when_unexpected_exit_code():
    # run should exit(2) when vm doesn't exist, so any exit code other than that
    with patch("qsm.dom0.lib.run", side_effect=lib.QsmProcessError(273863), autospec=True):
        with pytest.raises(lib.QsmProcessError):
            dom0.create("fedora-template", "red", exists_ok=True)


# >>> vm_prefs() >>>


def test_vm_prefs_executes_if_vm_exists():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
        # run returns None for successful run
        with patch("qsm.dom0.lib.run", return_value=None, autospec=True) as mock_run:
            dom0.vm_prefs("fedora-template", {"qrexec_timeout": "120"})
            assert mock_run.called, "run was not called, vm_prefs not executed"


def test_vm_prefs_throws_if_vm_doesnt_exist():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmDomainDoesntExistError, autospec=True):
        with pytest.raises(lib.QsmDomainDoesntExistError):
            dom0.vm_prefs("fedora-template", {"qrexec_timeout": "120"})


# >>> start() >>>


def test_start_executes_if_vm_exists():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
        # run returns None for successful run
        with patch("qsm.dom0.lib.run", return_value=None, autospec=True) as mock_run:
            dom0.start("fedora-template")
            assert mock_run.called, "run was not called, start not executed"


def test_start_throws_if_vm_doesnt_exist():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmDomainDoesntExistError, autospec=True):
        with pytest.raises(lib.QsmDomainDoesntExistError):
            dom0.start("fedora-template")

# >>> stop() >>>


def test_stop_executes_if_vm_exists_and_running():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
        with patch("qsm.dom0.is_running", return_value=True, autospec=True):
            # run returns None for successful run
            with patch("qsm.dom0.lib.run", return_value=None, autospec=True) as mock_run:
                dom0.stop("fedora-template")
                assert mock_run.called, "run was not called, stop not executed"


def test_stop_executes_if_vm_exists_and_not_running():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
        with patch("qsm.dom0.is_running", return_value=False, autospec=True):
            # run returns None for successful run
            with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
                # qvm-shutdown is never executed if the vm isn't running
                # so the function just completes without failure
                assert dom0.stop("fedora-template") is None


def test_stop_throws_if_vm_doesnt_exist():
    # exists_or_throws throws when vm doesn't exist
    with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmDomainDoesntExistError, autospec=True):
        with pytest.raises(lib.QsmDomainDoesntExistError):
            dom0.stop("fedora-template")

# >>> clone() >>>


def test_clone_executes_if_vm_exists():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):  # pass
        with patch("qsm.dom0.not_exists_or_throws", return_value=True, autospec=True):  # pass
            # run returns None for successful run
            with patch("qsm.dom0.lib.run", return_value=None, autospec=True) as mock_run:
                dom0.clone("fedora-template", "cloned-vm")
                assert mock_run.called, "run was not called, clone not executed"


def test_clone_throws_if_vm_doesnt_exist():
    # exists_or_throws throws when vm doesn't exist
    with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmDomainDoesntExistError, autospec=True):  # fails
        with patch("qsm.dom0.not_exists_or_throws", return_value=True, autospec=True):  # pass
            # run returns None for successful run
            with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
                with pytest.raises(lib.QsmDomainDoesntExistError):
                    dom0.clone("fedora-template", "cloned-vm")


def test_clone_throws_if_already_exist():
    # exists_or_throws throws when vm doesn't exist
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):  # pass
        with patch("qsm.dom0.not_exists_or_throws", side_effect=lib.QsmDomainAlreadyExistError, autospec=True):  # fail
            # run returns None for successful run
            with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
                with pytest.raises(lib.QsmDomainAlreadyExistError):
                    dom0.clone("fedora-template", "cloned-vm")


# >>> enable_services() >>>


def test_enable_services_executes_if_vm_exists():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
        # run returns None for successful run
        with patch("qsm.dom0.lib.run", return_value=None, autospec=True) as mock_run:
            dom0.enable_services(
                "fedora-template", ["service-one", "service-two"])
            assert mock_run.called, "run was not called, enable_services not executed"


def test_enable_services_throws_if_vm_doesnt_exist():
    # exists_or_throws throws when vm doesn't exist
    with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmDomainDoesntExistError, autospec=True):
        # run returns None for successful run
        with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
            with pytest.raises(lib.QsmDomainDoesntExistError):
                dom0.enable_services(
                    "fedora-template", ["service-one", "service-two"])

# >>> disable_services() >>>


def test_disable_services_executes_if_vm_exists():
    # exists_or_throws returns True when vm exists
    with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
        # run returns None for successful run
        with patch("qsm.dom0.lib.run", return_value=None, autospec=True) as mock_run:
            dom0.disable_services(
                "fedora-template", ["service-one", "service-two"])
            assert mock_run.called, "run was not called, disable_services not executed"


def test_disable_services_throws_if_vm_doesnt_exist():
    # exists_or_throws throws when vm doesn't exist
    with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmDomainDoesntExistError, autospec=True):
        # run returns None for successful run
        with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
            with pytest.raises(lib.QsmDomainDoesntExistError):
                dom0.disable_services(
                    "fedora-template", ["service-one", "service-two"])


# >>> create_vm() >>>

@patch("qsm.dom0.enable_services", return_value=None, autospec=True)
@patch("qsm.dom0.vm_prefs", return_value=None, autospec=True)
@patch("qsm.dom0.clone", return_value=None, autospec=True)
@patch("qsm.dom0.create", return_value=None, autospec=True)
def test_create_vm_happy_path(mock_create, mock_clone, mock_vm_prefs, mock_enable_services):
    dom0.create_vm("new-vm", "red")

    assert mock_create.called, "the vm was not created"
    assert not mock_clone.called, "the vm was cloned, instead of created"
    assert not mock_vm_prefs.called, "prefs were set, but none were given"
    assert not mock_enable_services.called, "services were enabled, but none were given"


@patch("qsm.dom0.enable_services", return_value=None, autospec=True)
@patch("qsm.dom0.vm_prefs", return_value=None, autospec=True)
@patch("qsm.dom0.clone", return_value=None, autospec=True)
@patch("qsm.dom0.create", return_value=None, autospec=True)
def test_create_vm_clone_from(mock_create, mock_clone, mock_vm_prefs, mock_enable_services):
    dom0.create_vm("new-vm", "red", clone_from="source-vm")

    assert not mock_create.called, "the vm was created, and not cloned"
    assert mock_clone.called, "the vm was not cloned"
    assert mock_vm_prefs.called, "prefs were not set, but a label should have been set"
    assert not mock_enable_services.called, "services were enabled, but none were given"


@patch("qsm.dom0.enable_services", return_value=None, autospec=True)
@patch("qsm.dom0.vm_prefs", return_value=None, autospec=True)
@patch("qsm.dom0.clone", return_value=None, autospec=True)
@patch("qsm.dom0.create", return_value=None, autospec=True)
def test_create_vm_prefs_are_set(mock_create, mock_clone, mock_vm_prefs, mock_enable_services):
    dom0.create_vm("new-vm", "red", prefs={"qrexec_timeout": 120})

    assert mock_create.called, "the vm was not created"
    assert not mock_clone.called, "the vm was cloned, instead of created"
    assert mock_vm_prefs.called, "prefs were not set, but one was given"
    assert not mock_enable_services.called, "services were enabled, but none were given"


@patch("qsm.dom0.enable_services", return_value=None, autospec=True)
@patch("qsm.dom0.vm_prefs", return_value=None, autospec=True)
@patch("qsm.dom0.clone", return_value=None, autospec=True)
@patch("qsm.dom0.create", return_value=None, autospec=True)
def test_create_vm_services_are_enabled(mock_create, mock_clone, mock_vm_prefs, mock_enable_services):
    dom0.create_vm("new-vm", "red", services=["service"])

    assert mock_create.called, "the vm was not created"
    assert not mock_clone.called, "the vm was cloned, instead of created"
    assert not mock_vm_prefs.called, "prefs were set, but none were given"
    assert mock_enable_services.called, "services were not enabled, but one was given"


@patch("qsm.dom0.enable_services", return_value=None, autospec=True)
@patch("qsm.dom0.vm_prefs", return_value=None, autospec=True)
@patch("qsm.dom0.clone", return_value=None, autospec=True)
@patch("qsm.dom0.create", return_value=None, autospec=True)
def test_create_vm_jobs_are_called(mock_create, mock_clone, mock_vm_prefs, mock_enable_services):
    _job_one = MagicMock()
    _job_two = MagicMock()
    _jobs = [lambda: _job_one(), lambda: _job_two()]
    dom0.create_vm("new-vm", "red", jobs=_jobs)

    assert mock_create.called, "the vm was not created"
    assert not mock_clone.called, "the vm was cloned, instead of created"
    assert not mock_vm_prefs.called, "prefs were set, but none were given"
    assert not mock_enable_services.called, "services were enabled, but none were given"

    assert _job_one.called, "job one wasn't called"
    assert _job_one.called, "job two wasn't called"


# >>> firewall() >>>
@pytest.mark.parametrize("do,expected", [
    # func | expected
    # action=accept
    (
        lambda: dom0.firewall("test-vm", "accept", "192.168.1.1", "1"),
        "qvm-firewall test-vm add action=accept dsthost=192.168.1.1 proto=tcp"
    ),
    # action=drop
    (
        lambda: dom0.firewall("test-vm", "drop", "192.168.1.1", "1"),
        "qvm-firewall test-vm add action=drop dsthost=192.168.1.1 proto=tcp"
    ),
    # proto=udp
    (
        lambda: dom0.firewall("test-vm", "accept", "192.168.1.1", "1", proto="udp"),
        "qvm-firewall test-vm add action=accept dsthost=192.168.1.1 proto=udp"
    ),
    # proto=icmp
    (
        lambda: dom0.firewall("test-vm", "accept", "192.168.1.1", "1", proto="icmp"),
        "qvm-firewall test-vm add action=accept dsthost=192.168.1.1 proto=icmp"
    ),
    # dsthost= (ipv4)/16
    (
        lambda: dom0.firewall("test-vm", "accept", "192.168.1.1/16", "1", proto="tcp"),
        "qvm-firewall test-vm add action=accept dsthost=192.168.1.1/16 proto=tcp"
    ),
    # dsthost = (ipv6)
    (
        lambda: dom0.firewall("test-vm", "accept", "4eeb:ac6d:1f62:f2c5:b84c:851a:bdac:9d0a", "1"),
        "qvm-firewall test-vm add action=accept dsthost=4eeb:ac6d:1f62:f2c5:b84c:851a:bdac:9d0a proto=tcp"
    ),
    # dsthost = (ipv6)/124
    (
        lambda: dom0.firewall("test-vm", "accept", "4eeb:ac6d:1f62:f2c5:b84c:851a:bdac:9d0a/124", "1"),
        "qvm-firewall test-vm add action=accept dsthost=4eeb:ac6d:1f62:f2c5:b84c:851a:bdac:9d0a/124 proto=tcp"
    ),
    # icmptype
    (
        lambda: dom0.firewall("test-vm", "accept", "192.168.1.1", "1", proto="icmp", icmptype=0),
        "qvm-firewall test-vm add action=accept dsthost=192.168.1.1 proto=icmp icmptype=0"
    ),
])
def test__firewall__happy_path(do, expected):
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True) as mock_run:
        with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
            do()
            assert re.search(expected, str(mock_run.call_args)), \
                "run was not called with expected args -- should be: {}".format(expected)


# ~~~ action ~~~
@hypothesis.given(s.one_of(s.integers(), s.text(), s.functions()))
def test__firewall__action__fuzz_negative(value):
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
            with pytest.raises(AssertionError):
                dom0.firewall("test-vm", value, "192.168.1.1", "1")


# ~~~ dsthost ~~~
@hypothesis.given(s.one_of(s.integers(), s.text(), s.functions()))
def test__firewall__dsthost__fuzz_negative(value):
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
            with pytest.raises(AssertionError):
                dom0.firewall("test-vm", "accept", value, "1")


# ~~~ dst ports ~~~
@hypothesis.given(s.one_of(s.floats(), s.text(), s.functions()))
def test__firewall__dstports__invalid_type_fuzz_negative(value):
    """Test random types cause assertion error"""
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
            with pytest.raises(AssertionError):
                dom0.firewall("test-vm", "accept", "192.168.1.1", value)


@hypothesis.given(s.integers(min_value=1, max_value=65535))
def test__firewall__dstports__fuzz_positive(value):
    """Test values inside of the acceptable range of ports"""
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
            assert dom0.firewall("test-vm", "accept", "192.168.1.1", str(value)) is None, \
                "{} should be accepted as a valid port".format(value)


@hypothesis.given(
    s.one_of(s.integers(min_value=65536, max_value=100000), s.integers(min_value=-100000, max_value=0)))
def test__firewall__dstports__fuzz_unacceptable_ints(value):
    """Test values outside of the acceptable range of ports."""
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
            with pytest.raises(AssertionError):
                dom0.firewall("test-vm", "accept", "192.168.1.1", str(value))


# ~~~ target ~~~
def test__firewall__target_doesnt_exist():
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmDomainDoesntExistError, autospec=True):
            with pytest.raises(lib.QsmDomainDoesntExistError):
                dom0.firewall("test-vm", "accept", "192.168.1.1", "1")


# ~~~ imcptype ~~~
@hypothesis.given(s.integers(min_value=0, max_value=43))
def test__firewall__icmptype__happy_fuzz(value):
    """Test values inside of the acceptable range of icmp types."""
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
            assert dom0.firewall("test-vm", "accept", "192.168.1.1", "1", proto="icmp", icmptype=value) is None


@hypothesis.given(
    s.one_of(s.integers(min_value=-100, max_value=-1), s.integers(min_value=44, max_value=100)))
def test__firewall__icmptype__nagative_fuzz(value):
    """Test values outside of the acceptable range of icmp types."""
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
            with pytest.raises(AssertionError):
                dom0.firewall("test-vm", "accept", "192.168.1.1", "1", proto="icmp", icmptype=value)


@hypothesis.given(s.one_of(s.text(), s.lists(s.integers()), s.booleans(), s.floats()))
def test__firewall__icmptype__invalid_type_nagative_fuzz(value):
    """Test non-integer types for icmptype - should throw."""
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
            with pytest.raises(AssertionError):
                dom0.firewall("test-vm", "accept", "192.168.1.1", "1", proto="icmp", icmptype=value)


def test__firewall__icmptype__proto_set_icmptype_is_used():
    """Test that proto must be icmp is icmptype is set"""
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
            with pytest.raises(AssertionError):
                dom0.firewall("test-vm", "accept", "192.168.1.1", "1", proto="tcp", icmptype=0)


# ~~~ proto ~~~
@hypothesis.given(s.one_of(s.text(), s.lists(s.integers()), s.booleans(), s.floats()))
def test__firewall__proto__invalid_type_nagative_fuzz(value):
    """Test invalid, unconstrained values for proto - should throw."""
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
            with pytest.raises(AssertionError):
                dom0.firewall("test-vm", "accept", "192.168.1.1", "1", proto=value)


@pytest.mark.parametrize("value", ["tcp", "udp", "icmp"])
def test__firewall__proto__happy_path(value):
    """Test valid, constrained values for proto"""
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        with patch("qsm.dom0.exists_or_throws", return_value=True, autospec=True):
            dom0.firewall("test-vm", "accept", "192.168.1.1", "1", proto=value) is None


# >>> is_template() >>>
# ~~~ is_template ~~~
def test__is_template__true():
    with patch("qsm.dom0.lib.run", return_value=None, autospec=True):
        assert dom0.is_template("test-template") is True


def test__is_template__false():
    with patch("qsm.dom0.lib.run", side_effect=lib.QsmProcessError(1), autospec=True):
        assert dom0.is_template("test-template") is False


# ~~~ is_template_or_throws ~~~
def test__is_template_or_throws__true():
    with patch("qsm.dom0.exists_or_throws", return_value=None, autospec=True):
        with patch("qsm.dom0.is_template", return_value=True, autospec=True):
            assert dom0.is_template_or_throws("test-template") is True


def test__is_template_or_throws__throws_when_vm_exists():
    """Test that it throws when the vm exists, but is not a template."""
    with patch("qsm.dom0.exists_or_throws", return_value=None, autospec=True):
        with patch("qsm.dom0.is_template", return_value=False, autospec=True):
            with pytest.raises(lib.QsmDomainIsNotATemplateError):
                dom0.is_template_or_throws("test-template")


def test__is_template_or_throws__throws_when_vm_not_exists():
    """Test that it throws when the vm does not exists"""
    with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmDomainDoesntExistError, autospec=True):
        with pytest.raises(lib.QsmDomainDoesntExistError):
            dom0.is_template_or_throws("test-template")


# ~~~ is_not_template_or_throws ~~~
def test__is_not_template_or_throws__true():
    """Test that a non-template is detected, but it's existence isn't evaluated"""
    with patch("qsm.dom0.is_template", return_value=False, autospec=True):
        assert dom0.is_not_template_or_throws("test-template", must_exist=False) is True


def test__is_not_template_or_throws__throws_when_domain_doesnt_exists():
    """Test that it throws when the domain doesn't exists at all"""
    with patch("qsm.dom0.exists_or_throws", side_effect=lib.QsmDomainDoesntExistError, autospec=True):
        with pytest.raises(lib.QsmDomainDoesntExistError):
            dom0.is_not_template_or_throws("test-template", must_exist=True)


def test__is_not_template_or_throws__passes_when_exists():
    """Test that it passes when the domain exists, and is a template."""
    with patch("qsm.dom0.exists_or_throws", return_value=None, autospec=True):
        with patch("qsm.dom0.is_template", return_value=False, autospec=True):
            assert dom0.is_not_template_or_throws("test-template", must_exist=True) is True


# >>> create_template() >>>
@patch("qsm.dom0.not_exists_or_throws", return_value=None, autospace=True)
@patch("qsm.dom0.exists", return_value=True, autospace=True)  # source_template
@patch("qsm.dom0.is_template_or_throws", return_value=True, autospace=True)
@patch("qsm.dom0.clone", return_value=None, autospace=True)
@patch("qsm.dom0.vm_prefs", return_value=None, autospace=True)
@patch("qsm.vm.update", return_value=None, autospace=True)
@patch("qsm.vm.install", return_value=None, autospace=True)
@patch("qsm.dom0.stop", return_value=None, autospace=True)
def test__create_template__happy_path(mock_stop, mock_install, mock_update, mock_vm_prefs, mock_clone, __, ___, ____):
    assert dom0.create_template("target-template", "source-template", update=False, shutdown=False) is None
    assert mock_clone.called is True, "clone was not called"
    assert mock_update.called is False, "the vm was updated"
    assert mock_install.called is False, "packages were installed in the vm"
    assert mock_stop.called is False, "the vm was stopped"
    assert mock_vm_prefs.call_count == 1, "prefs should have been called only once (to set the vm label)"
