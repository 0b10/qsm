import os

_targets = [
    "install",
    "update",
]

def get(target):
    assert target in _targets, "Invalid remote script; target doesn't exist"
    _dir = os.path.abspath(os.path.dirname(__file__))
    _target = os.path.join(_dir, "{}.py".format(target))
    with open(_target, "r") as f:
        return f.read()

