# MIT License
#
# Copyright (c) 2019 0b10
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from qsm.constants import GREEN, WHITE, RED, PURPLE, YELLOW
from subprocess import check_call, CalledProcessError
from qsm import constants
import re
import ipaddress

# TODO: fix user for dom0, use local user


def print_header(message):
    print(PURPLE + "+ " + message + "..." + WHITE)


def print_sub(message, failed=False):
    _colour = RED if failed else GREEN
    print(_colour + ">>> " + message + WHITE)


def print_sub_warning(message):
    print(YELLOW + ">>> " + message + WHITE)


def parse_packages(packages):
    return ' '.join(packages) if type(packages) is list else packages


def _run_dom0(command, target, user, show_message):
    _command = 'sudo --user={} {}'.format(user, command)
    try:
        check_call(_command, shell=True)
    except CalledProcessError as error:
        if show_message:
            print_sub("dom0 command: '{}'".format(_command), failed=True)
        raise QsmProcessError(error.returncode)


def _run_domU(command, target, user, show_message, colour=36, err_colour=36):
    # FIXME: qvm-run --pass-io seems to only pass to stderr, set both colours to the same value for now
    # the command has quotes, it works for all -c parameters that I know of
    _command = 'qvm-run --autostart --user {} --colour-output {} --colour-stderr {} --pass-io {} \"{}\"'.format(
        user, colour, err_colour, target, command)

    try:
        check_call(_command, shell=True)
    except CalledProcessError as error:
        if show_message:
            print_sub("qvm-run command for {}: '{}'".format(target,
                                                            _command), failed=True)
        raise QsmProcessError(error.returncode)


def run(command, target, user, show_message=True):
    if target == "dom0":
        _run_dom0(command, target, user, show_message)
    else:
        _run_domU(command, target, user, show_message)

# >>> PREDICATES >>>


def is_meaningful_string(value):
    return isinstance(value, str) and not re.search("^ *$", value)


def is_ip(value, network=True):
    if not isinstance(value, str):
        return False

    try:
        if network:
            ipaddress.ip_network(value, strict=False)
        else:
            ipaddress.ip_address(value)
    except (ipaddress.AddressValueError, ValueError):
        return False
    return True


def is_mac(value):
    assert isinstance(value, str), "mac address should be a string"
    return re.search(constants.RE_MAC_ADDRESS, value)


def assert_valid_dstports(value):
    assert isinstance(value, str), "dstports must be a string: {}".format(value)
    assert re.search("^[-,0-9]+$", value), \
        "invalid chars found for dstports - use '-' ',' or integers only: {}"
    ports = value.replace("-", ",").split(",")

    try:
        assert all([1 <= int(x) <= 65535 for x in ports]), \
            "dstport value must be between 1 - 65535: {}".format(value)
    except ValueError:
        raise AssertionError(
            "an uncastable (non-int like) value exists in dstports: {}".format(value))
    return True


class QsmProcessError(Exception):
    """
    Raised when a process returns a non-zero exit status.
    """

    def __init__(self, returncode):
        self.returncode = returncode


class QsmPreconditionError(Exception):
    """
    Raised when a precondition is not met.
    """
    pass


class QsmDomainRunningError(Exception):
    """
    Raised when a domain is running but it shouldn't be.
    """
    pass


class QsmDomainStoppedError(Exception):
    """
    Raised when a domain is stopped but it shouldn't be.
    """
    pass


class QsmDomainDoesntExistError(Exception):
    """
    Raised when a domain doesn't exist but it should.
    """
    pass


class QsmDomainAlreadyExistError(Exception):
    """
    Raised when a domain exists but it shouldn't.
    """
    pass


class QsmDomainIsNotATemplateError(Exception):
    """
    Raised when a domain is not a template, but should be.
    """
    pass


class QsmDomainIsATemplateError(Exception):
    """
    Raised when a domain is a template, but it shouldn't be.
    """
    pass
