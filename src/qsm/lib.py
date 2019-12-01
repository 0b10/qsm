from subprocess import check_call, CalledProcessError
from qsm.error import raise_process_error
from qsm.constants import GREEN, WHITE


def cprint(message, sub=False, colour=WHITE):
    if sub:
        print(colour + ">>> " + message + WHITE)
    else:
        print(colour + message + WHITE)


def print_success(message):
    cprint(message, sub=True, colour=GREEN)


def create(name, label, options=None):
    cprint("creating vm: {}".format(name))

    _options = "\b" if options is None else options
    try:
        check_call("qvm-create --label {} {} {}".format(label,
                                                        _options, name), shell=True)
    except CalledProcessError:
        raise_process_error()

    print_success("{} created".format(name))


def set_prefs(target, options):
    cprint("setting prefs for {}:".format(target))

    try:
        for _option, _value in options.items():
            check_call("qvm-prefs -s {} {} \'{}\'".format(target,
                                                          _option, _value), shell=True)
            print_success("{}: {}".format(_option, _value))
    except CalledProcessError:
        raise_process_error("- cannot set vm preferences")


def start(target):
    cprint("starting {}...".format(target))

    try:
        check_call("qvm-start --skip-if-running {}".format(target), shell=True)
    except CalledProcessError:
        raise_process_error("- unable to start vm")

    print_success("{} started".format(target))


def stop(target, timeout=120):
    cprint("stopping {}...".format(target))

    try:
        check_call(
            "qvm-shutdown --wait --timeout {} {}".format(timeout, target), shell=True)
    except CalledProcessError:
        raise_process_error("- unable to stop vm")

    print_success("{} stopped".format(target))


def remove(target):
    cprint("removing {}...".format(target))

    try:
        check_call("qvm-remove --force {}".format(target), shell=True)
    except CalledProcessError:
        raise_process_error("- unable to remove vm")

    print_success("{} removed".format(target))


def clone(source, target):
    cprint("cloning {} into {}...".format(source, target))

    try:
        check_call("qvm-clone {} {}".format(source, target), shell=True)
    except CalledProcessError:
        raise_process_error("- unable to remove vm")

    print_success("{} created".format(target))
