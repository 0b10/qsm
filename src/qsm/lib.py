from qsm.constants import GREEN, WHITE, RED, PURPLE
from subprocess import check_call, CalledProcessError
from qsm.error import raise_process_error


def print_header(message):
    print(PURPLE + "+ " + message + "..." + WHITE)


def print_sub(message, failed=False):
    _colour = RED if failed else GREEN
    print(_colour + ">>> " + message + WHITE)


def parse_packages(packages):
    return ' '.join(packages) if type(packages) is list else packages


def _run_dom0(command, target, user):
    _command = 'sudo --user={} {}'.format(user, command)
    try:
        check_call(_command, shell=True)
    except CalledProcessError:
        raise_process_error("dom0 command: '{}'".format(_command))

# TODO: --autostart, and refactor tests to use mock.call_args and re


def _run_domU(command, target, user, colour=36, err_colour=36):
    # FIXME: qvm-run --pass-io seems to only pass to stderr, set both to the same value for now
    # the command has quotes, it works for all -c parameters that I know of
    _command = 'qvm-run --autostart --user {} --colour-output {} --colour-stderr {} --pass-io {} \"{}\"'.format(
        user, colour, err_colour, target, command)

    try:
        check_call(_command, shell=True)
    except CalledProcessError:
        raise_process_error(
            "qvm-run command for {}: '{}'".format(target, _command))


def run(command, target, user):
    print_header("running command on {} as {}".format(target, user))

    if target == "dom0":
        _run_dom0(command, target, user)
    else:
        _run_domU(command, target, user)
