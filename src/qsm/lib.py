from qsm.constants import GREEN, WHITE, RED


def print_header(message):
    print(WHITE + message + "...")


def print_sub(message, failed=False):
    _colour = RED if failed else GREEN
    print(_colour + ">>> " + message + WHITE)
