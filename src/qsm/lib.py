from qsm.constants import GREEN, WHITE, RED, PURPLE, YELLOW
from subprocess import check_call, CalledProcessError


def print_header(message):
    print(PURPLE + "+ " + message + "..." + WHITE)


def print_sub(message, failed=False):
    _colour = RED if failed else GREEN
    print(_colour + ">>> " + message + WHITE)


def print_sub_warning(message):
    print(YELLOW + ">>> " + message + WHITE)


def parse_packages(packages):
    return ' '.join(packages) if type(packages) is list else packages


def _run_dom0(command, target, user, show_message):
    _command = 'sudo --user={} {}'.format(user, command)
    try:
        check_call(_command, shell=True)
    except CalledProcessError as error:
        if show_message:
            print_sub("dom0 command: '{}'".format(_command), failed=True)
        raise QsmProcessError(error.returncode)

# TODO: --autostart, and refactor tests to use mock.call_args and re


def _run_domU(command, target, user, show_message, colour=36, err_colour=36):
    # FIXME: qvm-run --pass-io seems to only pass to stderr, set both to the same value for now
    # the command has quotes, it works for all -c parameters that I know of
    _command = 'qvm-run --autostart --user {} --colour-output {} --colour-stderr {} --pass-io {} \"{}\"'.format(
        user, colour, err_colour, target, command)

    try:
        check_call(_command, shell=True)
    except CalledProcessError as error:
        if show_message:
            print_sub("qvm-run command for {}: '{}'".format(target,
                                                            _command), failed=True)
        raise QsmProcessError(error.returncode)


def run(command, target, user, show_message=True):
    if target == "dom0":
        _run_dom0(command, target, user, show_message)
    else:
        _run_domU(command, target, user, show_message)


class QsmProcessError(Exception):
    """
    Raised when a process returns a non-zero exit status.
    """
    def __init__(self, returncode):
        self.returncode = returncode


class QsmPreconditionError(Exception):
    """
    Raised when a precondition is not met.
    """
    pass


class QsmDomainRunningError(Exception):
    """
    Raised when a domain is running but it shouldn't be.
    """
    pass


class QsmDomainStoppedError(Exception):
    """
    Raised when a domain is stopped but it shouldn't be.
    """
    pass


class QsmDomainDoesntExistError(Exception):
    """
    Raised when a domain doesn't exist but it should.
    """
    pass


class QsmDomainAlreadyExistError(Exception):
    """
    Raised when a domain exists but it shouldn't.
    """
    pass
