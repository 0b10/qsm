from subprocess import check_call, CalledProcessError
from qsm.error import raise_process_error


def create(name, options=None):
    print("creating vm: {}".format(name))
    _options = "\b" if options is None else options
    try:
        check_call("qvm-create {} {}".format(_options, name), shell=True)
    except CalledProcessError:
        raise_process_error()


def set_prefs(target, options):
    print("setting prefs for {}:".format(target))
    try:
        for _option, _value in options.items():
            print(">>> {}: {}".format(_option, _value))
            check_call("qvm-prefs -s {} {} \'{}\'".format(target,
                                                          _option, _value), shell=True)
    except CalledProcessError:
        raise_process_error("- cannot set vm preferences")
