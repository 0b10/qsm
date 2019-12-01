from subprocess import check_call, CalledProcessError
from qsm.error import raise_process_error
from qsm.lib import print_header, print_sub
from qsm.constants import GREEN, WHITE, RED


def create(name, label, options=None):
    print_header("creating vm {}".format(name))

    _options = "\b" if options is None else options
    try:
        check_call("qvm-create --label {} {} {}".format(label,
                                                        _options, name), shell=True)
    except CalledProcessError:
        raise_process_error()

    print_sub("{} created".format(name))


def set_prefs(target, options):
    print_header("setting prefs for {}".format(target))

    try:
        for _option, _value in options.items():
            check_call("qvm-prefs -s {} {} \'{}\'".format(target,
                                                          _option, _value), shell=True)
            print_sub("{}: {}".format(_option, _value))
    except CalledProcessError:
        raise_process_error("- cannot set vm preferences")


def start(target):
    print_header("starting {}".format(target))

    try:
        check_call("qvm-start --skip-if-running {}".format(target), shell=True)
    except CalledProcessError:
        raise_process_error("- unable to start vm")

    print_sub("{} started".format(target))


def stop(target, timeout=120):
    print_header("stopping {}".format(target))

    try:
        check_call(
            "qvm-shutdown --wait --timeout {} {}".format(timeout, target), shell=True)
    except CalledProcessError:
        raise_process_error("- unable to stop vm")

    print_sub("{} stopped".format(target))


def remove(target):
    print_header("removing {}".format(target))

    try:
        check_call("qvm-remove --force {}".format(target), shell=True)
    except CalledProcessError:
        raise_process_error("- unable to remove vm")

    print_sub("{} removed".format(target))


def clone(source, target):
    print_header("cloning {} into {}".format(source, target))

    try:
        check_call("qvm-clone {} {}".format(source, target), shell=True)
    except CalledProcessError:
        raise_process_error("- unable to clone vm")

    print_sub("{} created".format(target))


def enable_services(target, services):
    print(GREEN+"enabling"+WHITE+" services on {}...".format(target))

    try:
        for _service in services:
            check_call("qvm-service --enable {}".format(_service), shell=True)
            print_sub("{}".format(_service))
    except CalledProcessError:
        raise_process_error("- unable to enable service")


def disable_services(target, services):
    print(RED+"disabling"+WHITE+" services on {}...".format(target))

    try:
        for _service in services:
            check_call("qvm-service --disable {}".format(_service), shell=True)
            print_sub("{}".format(_service))
    except CalledProcessError:
        raise_process_error("- unable to disable service")
