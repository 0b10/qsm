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
    # the command has quotes, it works for all -c parameters that I know of
    _command = 'qvm-run --user {} --pass-io {} \"{} \'{}\'\"'.format(
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

