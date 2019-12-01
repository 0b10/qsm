from subprocess import check_call, CalledProcessError
from qsm.error import raise_process_error


def create(name, options=None):
    _options = "\b" if options is None else options
    try:
        check_call("qvm-create {} {}".format(_options, name), shell=True)
    except CalledProcessError:
        raise_process_error()

