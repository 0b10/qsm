from subprocess import check_call, CalledProcessError
from .error import raise_process_error


def _run_dom0(command, target, user):
    _command = 'sudo --user={} {}'.format(user, command)
    try:
        check_call(_command, shell=True)
    except CalledProcessError:
        raise_process_error("dom0 command: '{}'".format(_command))

# TODO: --autostart, and refactor tests to use mock.call_args and re


def _run_domU(command, target, user):
    # the command has quotes, it works for all -c parameters that I know of
    _command = 'qvm-run --user {} --pass-io {} \"{}\"'.format(
        user, target, command)

    try:
        check_call(_command, shell=True)
    except CalledProcessError:
        raise_process_error("qvm-run command for {}: '{}'".format(target, _command))


def run(command, target, user):
    if target == "dom0":
        _run_dom0(command, target, user)
    else:
        _run_domU(command, target, user)
