from dpcontracts import require
import os

_targets = [
    "update"
]

@require("Invalid remote script; target doesn't exist", lambda args: args.target in _targets)
def get(target):
    _dir = os.path.abspath(os.path.dirname(__file__))
    _target = os.path.join(_dir, "{}.py".format(target))
    with open(_target, "r") as f:
        return f.read()

