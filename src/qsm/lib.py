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
import re
from qsm import constants

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
    # FIXME: qvm-run --pass-io seems to only pass to stderr, set both to the same value for now
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


def is_meaningful_string(value):
    return isinstance(value, str) and not re.search("^ *$", value)


def is_ipv4(value):
    if is_meaningful_string(value):
        try:
            _seg_bools = [int and int(x) >= 0 and int(x) <= 255 for x in value.split(".")]
        except ValueError:
            return False
        return len(_seg_bools) == 4 and all(_seg_bools)
    return False


class VmPrefsBuilder:
    def __init__(self):
        self._prefs = dict()

    def autostart(self, value=True):
        assert type(value) is bool, "autostart must be a bool"
        self._prefs["autostart"] = value
        return self

    def debug(self, value=True):
        assert type(value) is bool, "debug must be a bool"
        self._prefs["debug"] = value
        return self

    def default_dispvm(self, value):
        assert is_meaningful_string(
            value), "default_dispvm must be a non-empty string"
        self._prefs["default_dispvm"] = value
        return self

    def default_user(self, value):
        assert is_meaningful_string(
            value), "default_user must be a non-empty string"
        self._prefs["default_user"] = value
        return self

    def gateway(self, value):
        # TODO: contrain ip
        assert is_ipv4(value), "gateway should be an ipv4 address"
        self._prefs["gateway"] = value
        return self

    def gateway6(self, value):
        # TODO: constrain ipv6
        assert is_meaningful_string(
            value), "gateway6 must be a non-empty string"
        self._prefs["gateway6"] = value
        return self

    def include_in_backups(self, value=True):
        assert type(value) is bool, "include_in_backups must be a bool"
        self._prefs["include_in_backups"] = value
        return self

    def kernel(self, value):
        # TODO: regex, kernel version numbers
        assert is_meaningful_string(
            value), "kernel must be a non-empty string"
        self._prefs["kernel"] = value
        return self

    def kernel_opts(self, value):
        assert is_meaningful_string(
            value), "kernel_opts must be a non-empty string"
        self._prefs["kernel_opts"] = value
        return self

    def klass(self, value):
        # TODO: constrain
        assert is_meaningful_string(
            value), "klass must be a non-empty string"
        self._prefs["klass"] = value
        return self

    def label(self, value):
        # TODO: constrain to colours
        assert value in constants.LABELS, \
            "invalid label: '{}', must be one of: {}".format(value, constants.LABELS)
        self._prefs["label"] = value
        return self

    def mac(self, value):
        # TODO: constrain to mac address
        assert is_meaningful_string(
            value), "mac must be a non-empty string"
        self._prefs["mac"] = value
        return self

    def management_dispv(self, value):
        assert is_meaningful_string(
            value), "management_dispv must be a non-empty string"
        self._prefs["management_dispv"] = value
        return self

    def maxmem(self, value):
        # TODO: constrain, use __init__, share values
        assert isinstance(
            value, int) and value > 0, "maxmem must be an integer > 0"
        self._prefs["maxmem"] = value
        return self

    def memory(self, value):
        # TODO: constrain, use __init__, share values
        assert isinstance(
            value, int) and value > 0, "memory must be an integer > 0"
        self._prefs["memory"] = value
        return self

    def name(self, value):
        assert is_meaningful_string(
            value), "name must be a non-empty string"
        self._prefs["name"] = value
        return self

    def netvm(self, value):
        assert is_meaningful_string(
            value), "netvm must be a non-empty string"
        self._prefs["netvm"] = value
        return self

    def provides_network(self, value=True):
        assert type(value) is bool, "provides_network must be a bool"
        self._prefs["provides_network"] = value
        return self

    def qrexec_timeout(self, value=120):
        assert isinstance(
            value, int) and value > 0, "qrexec_timeout must be an integer > 0"
        self._prefs["qrexec_timeout"] = value
        return self

    def shutdown_timeout(self, value=120):
        assert isinstance(
            value, int) and value > 0, "shutdown_timeout must be an integer > 0"
        self._prefs["shutdown_timeout"] = value
        return self

    def template(self, value):
        assert is_meaningful_string(
            value), "template must be a non-empty string"
        self._prefs["template"] = value
        return self

    def template_for_dispvms(self, value=True):
        assert type(value) is bool, "template_for_dispvms must be a bool"
        self._prefs["template_for_dispvms"] = value
        return self

    def updateable(self, value=True):
        assert type(value) is bool, "updateable must be a bool"
        self._prefs["updateable"] = value
        return self

    def uuid(self, value):
        # TODO: constrain by uuid
        assert is_meaningful_string(
            value), "uuid must be a non-empty string"
        self._prefs["uuid"] = value
        return self

    def vcpus(self, value=4):
        assert isinstance(
            value, int) and value > 0, "vcpus must be an integer > 0"
        self._prefs["vcpus"] = value
        return self

    def virt_mode(self, value):
        # TODO: constrain by virt modes
        assert is_meaningful_string(
            value), "virt_mode must be a non-empty string"
        self._prefs["virt_mode"] = value
        return self

    def visible_gateway(self, value):
        assert is_ipv4(value), \
            "visible_gateway should be an ipv4 address: {}".format(value)
        self._prefs["visible_gateway"] = value
        return self

    def visible_gateway6(self, value):
        # TODO: constrain by IP
        assert is_meaningful_string(
            value), "visible_gateway6 must be a non-empty string"
        self._prefs["visible_gateway6"] = value
        return self

    def visible_ip(self, value):
        assert is_ipv4(value), \
            "visible_ip should be an ipv4 address: {}".format(value)
        self._prefs["visible_ip"] = value
        return self

    def visible_ip6(self, value):
        # TODO: constrain by IP
        assert is_meaningful_string(
            value), "visible_ip6 must be a non-empty string"
        self._prefs["visible_ip6"] = value
        return self

    def visible_netmask(self, value):
        assert is_ipv4(value), \
            "visible_netmask is invalid: {}".format(value)
        assert is_meaningful_string(
            value), "visible_netmask must be a non-empty string"
        self._prefs["visible_netmask"] = value
        return self
