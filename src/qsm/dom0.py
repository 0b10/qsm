from qsm.lib import (print_header, print_sub, parse_packages, run, QsmPreconditionError, QsmProcessError,
                     print_sub_warning)
from qsm.constants import GREEN, WHITE, RED, QVM_CHECK_EXISTS_NOT_FOUND


def exists(target):
    _command = "qvm-check --quiet {} >/dev/null".format(target)
    try:
        run(command=_command, target="dom0", user="root")
    except QsmProcessError as error:
        if error.returncode != QVM_CHECK_EXISTS_NOT_FOUND:
            print_sub("a problem occurred when checking if {} exists".format(
                target), failed=True)
            raise error
        return False
    return True


def exists_or_throws(target, message=None):
    _message = "{} doesn't exist" if message is None else message

    if not exists(target):
        print_sub(_message, failed=True)
        raise QsmPreconditionError

    return True


def is_running(target):
    _command = "qvm-check --quiet --running {} >/dev/null".format(
        target)
    try:
        run(command=_command, target="dom0", user="root")
    except QsmProcessError as error:
        if error.returncode != 1:  # 1 is "domain is running"
            print_sub("a problem occurred when checking if {} is running".format(
                target), failed=True)
            raise error
        return False
    return True


def is_running_or_throws(target, message=None):
    _message = "{} is not running" if message is None else message

    if is_running(target):
        return True

    print_sub(_message, failed=True)
    raise QsmPreconditionError


def is_stopped_or_throws(target, message=None):
    _message = "{} is running" if message is None else message

    if is_running(target):
        print_sub(_message, failed=True)
        raise QsmPreconditionError

    return True


def create(name, label, options=None, exists_ok=True):
    print_header("creating vm {}".format(name))

    _options = "\b" if options is None else options
    _command = "qvm-create --label {} {} {}".format(label, _options, name)

    if exists_ok:
        try:
            run(command=_command, target="dom0", user="root")
        except QsmProcessError as error:
            if error.returncode != 1:  # 1 is "already exists"
                raise error
    else:
        exists_or_throws(name)
        # only reachable if exists
        print_sub_warning("{} already exists, using that".format(name))

    print_sub("{} creation finished".format(name))


def vm_prefs(target, prefs):
    print_header("setting prefs for {}".format(target))
    exists_or_throws(target)

    for _key, _value in prefs.items():
        _command = "qvm-prefs -s {} {} \'{}\'".format(target, _key, _value)
        run(command=_command, target="dom0", user="root")

        print_sub("{}: {}".format(_key, _value))


def start(target):
    print_header("starting {}".format(target))
    exists_or_throws(target)

    _command = "qvm-start --skip-if-running {}".format(target)
    run(command=_command, target="dom0", user="root")

    print_sub("{} started".format(target))


def stop(target, timeout=120):
    exists_or_throws(target)

    print_header("stopping {}".format(target))

    if is_running(target):
        _command = "qvm-shutdown --wait --timeout {} {}".format(
            timeout, target)
        run(command=_command, target="dom0", user="root")

        print_sub("{} stopped".format(target))
        return

    print_sub_warning("{} already stopped".format(target))


def remove(target, shutdown_ok=False):
    print_header("removing {}".format(target))

    if shutdown_ok:
        stop(target)
    else:
        is_stopped_or_throws(target)

    _command = "qvm-remove --quiet --force {}".format(target)
    if exists(target):  # pep.. shhh
        run(command=_command, target="dom0", user="root")

    print_sub("{} removal finished".format(target))


def clone(source, target):
    print_header("cloning {} into {}".format(source, target))
    exists_or_throws(source)

    _command = "qvm-clone {} {}".format(source, target)
    run(command=_command, target="dom0", user="root")

    print_sub("{} created".format(target))


def enable_services(target, services):
    print(GREEN+"enabling"+WHITE+" services on {}...".format(target))
    exists_or_throws(target)

    for _service in services:
        _command = "qvm-service --enable {}".format(_service)
        run(command=_command, target="dom0", user="root")

        print_sub("{}".format(_service))


def disable_services(target, services):
    print(RED+"disabling"+WHITE+" services on {}...".format(target))
    exists_or_throws(target)

    for _service in services:
        _command = "qvm-service --disable {}".format(_service)
        run(command=_command, target="dom0", user="root")

        print_sub("{}".format(_service))


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
