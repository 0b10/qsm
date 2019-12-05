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
from qsm import lib, constants
import types


# >>> PREDICATES >>>

def exists(target):
    _command = "qvm-check --quiet {} 2>/dev/null".format(target)
    try:
        lib.run(command=_command, target="dom0",
                user="root", show_message=False)
    except lib.QsmProcessError as error:
        if error.returncode != constants.QVM_CHECK_EXISTS_NOT_FOUND:  # is not exit code 2
            # some other error occurred
            lib.print_sub("a problem occurred when checking that {} exists".format(
                target), failed=True)
            raise error
        return False  # is exit code 2 == domain doesn't exist
    return True


def exists_or_throws(target, message=None):
    _message = "{} doesn't exist".format(
        target) if message is None else message

    if exists(target):
        return True

    lib.print_sub(_message, failed=True)
    raise lib.QsmDomainDoesntExistError


def not_exists_or_throws(target, message=None):
    _message = "{} already exist".format(
        target) if message is None else message

    if not exists(target):
        return True

    lib.print_sub(_message, failed=True)
    raise lib.QsmDomainAlreadyExistError


def is_running(target):
    _command = "qvm-check --quiet --running {} 2>/dev/null".format(
        target)
    try:
        lib.run(command=_command, target="dom0",
                user="root", show_message=False)
    except lib.QsmProcessError as error:
        if error.returncode != constants.QVM_CHECK_IS_NOT_RUNNING:  # is not exit code 1
            # some other error occurred
            lib.print_sub("a problem occurred when checking that {} is running".format(
                target), failed=True)
            raise error
        return False  # is exit code 1 == domain is not running
    return True


def is_running_or_throws(target, message=None):
    _message = "{} is not running".format(
        target) if message is None else message

    if is_running(target):
        return True

    lib.print_sub(_message, failed=True)
    raise lib.QsmDomainStoppedError


def is_stopped_or_throws(target, message=None):
    _message = "{} is running".format(target) if message is None else message

    if is_running(target):
        lib.print_sub(_message, failed=True)
        raise lib.QsmDomainRunningError

    return True


# >>> DOMAIN PROVISIONING >>>

def create(name, label, options="", exists_ok=True):
    lib.print_header("creating vm {}".format(name))

    _command = "qvm-create --quiet --label {} {} {} 2>/dev/null".format(
        label, options, name)

    if exists_ok:
        try:
            lib.run(command=_command, target="dom0",
                    user="root", show_message=False)
        except lib.QsmProcessError as error:
            if error.returncode != constants.QVM_CREATE_DOMAIN_ALREADY_EXISTS:  # is not exit code 1
                # some other error occurred
                raise error
            lib.print_sub_warning("{} already exists, using that".format(name))
            return
    else:
        not_exists_or_throws(name)
        lib.run(command=_command, target="dom0",
                user="root", show_message=False)

    lib.print_sub("{} creation finished".format(name))


def vm_prefs(target, prefs):
    assert type(prefs) is dict, "prefs should be a dict"

    lib.print_header("setting prefs for {}".format(target))
    exists_or_throws(target)

    for _key, _value in prefs.items():
        _command = "qvm-prefs -s {} {} \'{}\'".format(target, _key, _value)
        lib.run(command=_command, target="dom0",
                user="root", show_message=False)

        lib.print_sub("{}: {}".format(_key, _value))


def start(target):
    lib.print_header("starting {}".format(target))
    exists_or_throws(target)

    _command = "qvm-start --skip-if-running {}".format(target)
    lib.run(command=_command, target="dom0", user="root", show_message=False)

    lib.print_sub("{} started".format(target))


def stop(target, timeout=120):
    lib.print_header("stopping {}".format(target))
    exists_or_throws(target)

    if is_running(target):
        _command = "qvm-shutdown --wait --timeout {} {}".format(
            timeout, target)
        lib.run(command=_command, target="dom0",
                user="root", show_message=False)

        lib.print_sub("{} stopped".format(target))
        return

    lib.print_sub_warning("{} already stopped".format(target))


def remove(target, shutdown_ok=False):
    lib.print_header("removing {}".format(target))

    _command = "qvm-remove --quiet --force {}".format(target)
    if exists(target):  # pep.. shhh
        if shutdown_ok:
            stop(target)
        else:
            is_stopped_or_throws(target)
        lib.run(command=_command, target="dom0",
                user="root", show_message=False)

        lib.print_sub("{} removal finished".format(target))
        return

    lib.print_sub_warning("{} doesn't exist, continuing...".format(target))


def clone(source, target):
    lib.print_header("cloning {} into {}".format(source, target))
    exists_or_throws(source)
    not_exists_or_throws(target)

    _command = "qvm-clone --quiet {} {} 2>/dev/null".format(source, target)
    lib.run(command=_command, target="dom0", user="root", show_message=False)

    lib.print_sub("{} created".format(target))


def enable_services(target, services):
    assert type(services) is list, "services should be a list"

    lib.print_header("enabling services on {}...".format(target))
    exists_or_throws(target)

    for _service in services:
        _command = "qvm-service --enable {} {}".format(target, _service)
        lib.run(command=_command, target="dom0",
                user="root", show_message=False)

        lib.print_sub("{}".format(_service))


def disable_services(target, services):
    assert type(services) is list, "services should be a list"

    lib.print_header("disabling services on {}...".format(target))
    exists_or_throws(target)

    for _service in services:
        _command = "qvm-service --disable {} {}".format(
            target, _service, show_message=False)
        lib.run(command=_command, target="dom0",
                user="root", show_message=False)

        lib.print_sub("{}".format(_service))


def firewall(target, action, dsthost, dstports, icmptype=None, proto="tcp"):
    assert exists_or_throws(target)
    assert action in ["accept", "drop"], \
        "action should be accept or drop: {}".format(action)
    lib.assert_valid_dstports(dstports)
    assert lib.is_ip(dsthost, network=True), \
        "dsthost should be a valid ip address: {}".format(dsthost)
    assert proto in ["tcp", "udp", "icmp"], \
        "proto must be icmp, tcp, or udp: {}".format(proto)

    _command = "qvm-firewall {0} add action={1} dsthost={2} proto={3}"\
        .format(target, action, dsthost, proto)

    if icmptype is not None:
        assert type(icmptype) is int and 0 <= icmptype <= 43, \
            "icmptype must be an integer, 0 <= n <= 43: {}".format(icmptype)
        assert proto == \
            "icmp", "proto must be icmp if setting icmp type: {}".format(proto)
        _command += " icmptype={}".format(icmptype)

    lib.run(_command, target, "user", show_message=False)


# >>> PACKAGE MANAGER >>>


def update():
    lib.print_header("updating dom0")

    lib.run(command="qubes-dom0-update -y", target="dom0", user="root")

    lib.print_sub("dom0 update finished")


def install(packages):
    lib.print_header("installing packages on dom0")

    _command = "qubes-dom0-update -y {}".format(
        lib.parse_packages(packages))
    lib.run(command=_command, target="dom0", user="root")

    lib.print_sub("dom0 package installation finished")


def uninstall(packages):
    lib.print_header("uninstalling packages from dom0")

    _command = "qubes-dom0-update --action=remove -y {}".format(
        lib.parse_packages(packages))
    lib.run(command=_command, target="dom0", user="root")

    lib.print_sub("dom0 package uninstallation finished")


# >>> CONVENIENCE FUNCTIONS >>>
def _is_all_funcs(list_):
    return type(list_) is list and all([isinstance(item, types.FunctionType) for item in list_])


def _merge_prefs(prefs, label):
    _label = {"label": label}
    return {**prefs, **_label} if prefs else _label


def create_vm(name, label, clone_from=None, prefs=None, services=None, jobs=None, exists_ok=True):
    assert type(
        prefs) is dict or prefs is None, "prefs should be a dict, or None"

    _prefs = prefs

    if clone_from:
        clone(clone_from, name)
        _prefs = _merge_prefs(prefs, label)  # set label
    else:
        create(name, label, exists_ok=True)

    if _prefs:
        vm_prefs(name, _prefs)

    if services:
        enable_services(name, services)

    if jobs:
        assert _is_all_funcs(jobs), \
            "jobs should be a list of funcs/lambdas, that take no params: [lambda: my_func(param), ...]"
        for job in jobs:
            job()
