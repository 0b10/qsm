import os
import platform
from subprocess import call

_commands = {
    "fedora": "dnf update -y",
    "debian": "apt-get upgrade -y",
}

_dist = platform.dist()[0]
_command = _commands[_dist]

call(_command, shell=True)
