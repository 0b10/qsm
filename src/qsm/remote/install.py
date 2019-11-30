import os
import platform
from subprocess import call
import sys

_packages = sys.argv[1]

_commands = {
    "fedora": "dnf install -y {}".format(_packages),
    "debian": "apt-get install -y {}".format(_packages),
}

_dist = platform.dist()[0]
_command = _commands[_dist]

call(_command, shell=True)
