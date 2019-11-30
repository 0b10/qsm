from subprocess import check_call, CalledProcessError
from .error import process_error

_shells = {
    # TODO: how would these handle a script path?
    "bash": "bash -c",
    "zsh": "zsh -c"
}


def _run_dom0(command, target, user, shell):
    _command = 'sudo --user={} {} {}'.format(user,
                                             _shells.get(shell, shell), command)
    try:
        check_call(_command, shell=True)
    except CalledProcessError as error:
        process_error("dom0 shell command: '{}'".format(_command))

# TODO: --autostart, and refactor tests to use mock.call_args and re


def _run_domU(command, target, user, shell):
    _command = 'qvm-run --user {} --pass-io {} \"{} {}\"'.format(
        user, target, _shells.get(shell, shell), command)

    try:
        check_call(_command, shell=True)
    except CalledProcessError as error:
        process_error("qvm-run command for {}: '{}'".format(target, _command))


def run(command, target, user, shell="bash"):
    if target == "dom0":
        _run_dom0(command, target, user, shell)
    else:
        _run_domU(command, target, user, shell)


def _quotify(args):
    return ' '.join("\'{}\'".format(x) for x in args) if args else None


def run_remote(command, target, user, args=None):
    assert type(args) is list or args is None, "args should be a list, or None"
    # surround with quotations, else None
    _args = _quotify(args)  # "'arg1', 'arg2'"

    if args:
        _command = 'qvm-run --user {} --pass-io {} \"python3 -c \'{}\' {}\"'.format(
            user, target, command, _args) # args doesn't need quotations, _quotify quotes each separately
    else:
        _command = 'qvm-run --user {} --pass-io {} \"python3 -c \'{}\'\"'.format(
            user, target, command)

    try:
        check_call(_command, shell=True)
    except CalledProcessError as error:
        process_error(
            "qvm-run remote python script for {}: '{}'".format(target, _command))
