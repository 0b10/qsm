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
from qsm import lib
from qsm.remote import install as install_script, update as update_script, remove as remove_script
from qsm.lib import print_header, print_sub, parse_packages
import re
from qsm import constants


def update(target):
    print_header("updating {}".format(target))

    lib.run(command=update_script(), target=target, user="root")

    print_sub("{} update finished".format(target))


def install(target, packages):
    print_header("installing packages on {}".format(target))

    _packages = parse_packages(packages)
    lib.run(command=install_script(_packages), target=target, user="root")

    print_sub("{} package installation finished".format(target))


def uninstall(target, packages):
    print_header("removing packages from {}".format(target))

    _packages = parse_packages(packages)
    lib.run(command=remove_script(_packages), target=target, user="root")

    print_sub("{} package uninstallation finished".format(target))


class VmPrefsBuilder:
    def __init__(self):
        self._prefs = dict({"memory": 400, "maxmem": 1000})

    def autostart(self, value=True):
        assert type(value) is bool, "autostart must be a bool: {}".format(value)
        self._prefs["autostart"] = value
        return self

    def debug(self, value=True):
        assert type(value) is bool, "debug must be a bool: {}".format(value)
        self._prefs["debug"] = value
        return self

    def default_dispvm(self, value):
        assert lib.is_meaningful_string(value), \
            "default_dispvm must be a non-empty string: {}".format(value)
        self._prefs["default_dispvm"] = value
        return self

    def default_user(self, value):
        assert lib.is_meaningful_string(value), \
            "default_user must be a non-empty string: {}".format(value)
        self._prefs["default_user"] = value
        return self

    def include_in_backups(self, value=True):
        assert type(value) is bool, \
            "include_in_backups must be a bool: {}".format(value)
        self._prefs["include_in_backups"] = value
        return self

    def kernel(self, value):
        assert re.search(constants.RE_KERNEL_VERSION, value), \
            "kernel should be numbers, dots, and dashes: {}".format(
                value)
        self._prefs["kernel"] = value
        return self

    def kernel_opts(self, value):
        assert lib.is_meaningful_string(value), \
            "kernel_opts must be a non-empty string: {}".format(value)
        self._prefs["kernel_opts"] = value
        return self

    def label(self, value):
        assert value in constants.LABELS, \
            "invalid label: '{}', must be one of: {}".format(
                value, constants.LABELS)
        self._prefs["label"] = value
        return self

    def mac(self, value):
        assert lib.is_mac(value), \
            "mac must be a mac address: {}".format(value)
        self._prefs["mac"] = value
        return self

    def management_dispv(self, value):
        assert lib.is_meaningful_string(value), \
            "management_dispv must be a non-empty string: {}".format(value)
        self._prefs["management_dispv"] = value
        return self

    def maxmem(self, value):
        assert isinstance(value, int) and value > 0, \
            "maxmem must be an integer > 0: {}".format(value)
        self._prefs["maxmem"] = value
        return self

    def memory(self, value):
        assert isinstance(value, int) and value > 0, \
            "memory must be an integer > 0: {}".format(value)
        self._prefs["memory"] = value
        return self

    def name(self, value):
        assert lib.is_meaningful_string(value), \
            "name must be a non-empty string: {}".format(value)
        self._prefs["name"] = value
        return self

    def netvm(self, value):
        assert lib.is_meaningful_string(value), \
            "netvm must be a non-empty string: {}".format(value)
        self._prefs["netvm"] = value
        return self

    def provides_network(self, value=True):
        assert type(value) is bool, \
            "provides_network must be a bool: {}".format(value)
        self._prefs["provides_network"] = value
        return self

    def qrexec_timeout(self, value=120):
        assert isinstance(value, int) and value > 0, \
            "qrexec_timeout must be an integer > 0: {}".format(
                value)
        self._prefs["qrexec_timeout"] = value
        return self

    def shutdown_timeout(self, value=120):
        assert isinstance(value, int) and value > 0, \
            "shutdown_timeout must be an integer > 0: {}".format(value)
        self._prefs["shutdown_timeout"] = value
        return self

    def template(self, value):
        assert lib.is_meaningful_string(value), \
            "template must be a non-empty string: {}".format(value)
        self._prefs["template"] = value
        return self

    def template_for_dispvms(self, value=True):
        assert type(value) is bool, \
            "template_for_dispvms must be a bool: {}".format(value)
        self._prefs["template_for_dispvms"] = value
        return self

    def vcpus(self, value=4):
        assert type(value) is int and value > 0, \
            "vcpus must be an integer > 0: {}".format(value)
        self._prefs["vcpus"] = value
        return self

    def virt_mode(self, value):
        assert value in constants.VIRT_MODES, \
            "virt_mode is invalid: {}, must be one of: {}".format(
                value, constants.VIRT_MODES)
        self._prefs["virt_mode"] = value
        return self

    def build(self):
        # check maxmem > memory here because it means they can be specified in any order
        _maxmem = self._prefs["maxmem"]
        _memory = self._prefs["memory"]
        assert _maxmem > _memory, \
            "maxmem must be greater than memory -- maxmem: {}, memory: {}".format(
                _maxmem, _memory)

        return self._prefs
