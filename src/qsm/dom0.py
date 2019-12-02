from qsm.lib import (print_header, print_sub, parse_packages, run, QsmPreconditionError, QsmProcessError,
                     print_sub_warning)
from qsm.constants import GREEN, WHITE, RED


def exists(target):
    _command = "qvm-check --quiet {} > 2&>1 >/dev/null"
    try:
        run(command=_command, target="dom0", user="root")
    except QsmProcessError as error:
        if error.returncode == 2:  # 2 is "domain not found"
            return False
        else:
            raise error  # something else went wrong
    return True


def exists_or_throws(target, message=None):
    _message = "{} doesn't exist" if message is None else message

    if not exists(target):
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
    print_header("stopping {}".format(target))
    exists_or_throws(target)

    _command = "qvm-shutdown --wait --timeout {} {}".format(timeout, target)
    run(command=_command, target="dom0", user="root")

    print_sub("{} stopped".format(target))


# TODO: check not running, shutdown first
def remove(target):
    print_header("removing {}".format(target))

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
