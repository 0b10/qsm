from qsm.lib import (print_header, print_sub, parse_packages, run, QsmProcessError,
                     print_sub_warning, QsmDomainDoesntExistError, QsmDomainAlreadyExistError,
                     QsmDomainRunningError, QsmDomainStoppedError)
from qsm.constants import (QVM_CHECK_EXISTS_NOT_FOUND, QVM_CHECK_IS_NOT_RUNNING,
                           QVM_CREATE_DOMAIN_ALREADY_EXISTS)
import types


# >>> PREDICATES >>>

def exists(target):
    _command = "qvm-check --quiet {} 2>/dev/null".format(target)
    try:
        run(command=_command, target="dom0", user="root", show_message=False)
    except QsmProcessError as error:
        if error.returncode != QVM_CHECK_EXISTS_NOT_FOUND:  # is not exit code 2
            # some other error occurred
            print_sub("a problem occurred when checking that {} exists".format(
                target), failed=True)
            raise error
        return False  # is exit code 2 == domain doesn't exist
    return True


def exists_or_throws(target, message=None):
    _message = "{} doesn't exist".format(
        target) if message is None else message

    if exists(target):
        return True

    print_sub(_message, failed=True)
    raise QsmDomainDoesntExistError


def not_exists_or_throws(target, message=None):
    _message = "{} already exist".format(
        target) if message is None else message

    if not exists(target):
        return True

    print_sub(_message, failed=True)
    raise QsmDomainAlreadyExistError


def is_running(target):
    _command = "qvm-check --quiet --running {} 2>/dev/null".format(
        target)
    try:
        run(command=_command, target="dom0", user="root", show_message=False)
    except QsmProcessError as error:
        if error.returncode != QVM_CHECK_IS_NOT_RUNNING:  # is not exit code 1
            # some other error occurred
            print_sub("a problem occurred when checking that {} is running".format(
                target), failed=True)
            raise error
        return False  # is exit code 1 == domain is not running
    return True


def is_running_or_throws(target, message=None):
    _message = "{} is not running".format(
        target) if message is None else message

    if is_running(target):
        return True

    print_sub(_message, failed=True)
    raise QsmDomainStoppedError


def is_stopped_or_throws(target, message=None):
    _message = "{} is running".format(target) if message is None else message

    if is_running(target):
        print_sub(_message, failed=True)
        raise QsmDomainRunningError

    return True


# >>> DOMAIN PROVISIONING >>>

def create(name, label, options="", exists_ok=True):
    print_header("creating vm {}".format(name))

    _command = "qvm-create --quiet --label {} {} {} 2>/dev/null".format(
        label, options, name)

    if exists_ok:
        try:
            run(command=_command, target="dom0",
                user="root", show_message=False)
        except QsmProcessError as error:
            if error.returncode != QVM_CREATE_DOMAIN_ALREADY_EXISTS:  # is not exit code 1
                # some other error occurred
                raise error
            print_sub_warning("{} already exists, using that".format(name))
            return
    else:
        not_exists_or_throws(name)
        run(command=_command, target="dom0", user="root", show_message=False)

    print_sub("{} creation finished".format(name))


def vm_prefs(target, prefs):
    assert type(prefs) is dict, "prefs should be a dict"

    print_header("setting prefs for {}".format(target))
    exists_or_throws(target)

    for _key, _value in prefs.items():
        _command = "qvm-prefs -s {} {} \'{}\'".format(target, _key, _value)
        run(command=_command, target="dom0", user="root", show_message=False)

        print_sub("{}: {}".format(_key, _value))


def start(target):
    print_header("starting {}".format(target))
    exists_or_throws(target)

    _command = "qvm-start --skip-if-running {}".format(target)
    run(command=_command, target="dom0", user="root", show_message=False)

    print_sub("{} started".format(target))


def stop(target, timeout=120):
    print_header("stopping {}".format(target))
    exists_or_throws(target)

    if is_running(target):
        _command = "qvm-shutdown --wait --timeout {} {}".format(
            timeout, target)
        run(command=_command, target="dom0", user="root", show_message=False)

        print_sub("{} stopped".format(target))
        return

    print_sub_warning("{} already stopped".format(target))


def remove(target, shutdown_ok=False):
    print_header("removing {}".format(target))

    _command = "qvm-remove --quiet --force {}".format(target)
    if exists(target):  # pep.. shhh
        if shutdown_ok:
            stop(target)
        else:
            is_stopped_or_throws(target)
        run(command=_command, target="dom0", user="root", show_message=False)

        print_sub("{} removal finished".format(target))
        return

    print_sub_warning("{} doesn't exist, continuing...".format(target))


def clone(source, target):
    print_header("cloning {} into {}".format(source, target))
    exists_or_throws(source)
    not_exists_or_throws(target)

    _command = "qvm-clone --quiet {} {} 2>/dev/null".format(source, target)
    run(command=_command, target="dom0", user="root", show_message=False)

    print_sub("{} created".format(target))


def enable_services(target, services):
    assert type(services) is list, "services should be a list"

    print_header("enabling services on {}...".format(target))
    exists_or_throws(target)

    for _service in services:
        _command = "qvm-service --enable {} {}".format(target, _service)
        run(command=_command, target="dom0", user="root", show_message=False)

        print_sub("{}".format(_service))


def disable_services(target, services):
    assert type(services) is list, "services should be a list"

    print_header("disabling services on {}...".format(target))
    exists_or_throws(target)

    for _service in services:
        _command = "qvm-service --disable {} {}".format(
            target, _service, show_message=False)
        run(command=_command, target="dom0", user="root", show_message=False)

        print_sub("{}".format(_service))


# >>> PACKAGE MANAGER >>>

def update():
    print_header("updating dom0")

    run(command="qubes-dom0-update -y", target="dom0", user="root")

    print_sub("dom0 update finished")


def install(packages):
    print_header("installing packages on dom0")

    _command = "qubes-dom0-update -y {}".format(
        parse_packages(packages))
    run(command=_command, target="dom0", user="root")

    print_sub("dom0 package installation finished")


def uninstall(packages):
    print_header("uninstalling packages from dom0")

    _command = "qubes-dom0-update --action=remove -y {}".format(
        parse_packages(packages))
    run(command=_command, target="dom0", user="root")

    print_sub("dom0 package uninstallation finished")


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
