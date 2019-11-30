from textwrap import dedent


def install(packages):
    return dedent("""\
        import os
        import platform
        from subprocess import call
        import sys

        _commands = {
            \"fedora\": \"dnf install -y {0}\",
            \"debian\": \"apt-get install -y {0}\"
        }

        _dist = platform.dist()[0]
        _command = _commands[_dist]

        call(_command, shell=True)
    """.format(packages))


def update():
    return dedent("""\
        import os
        import platform
        from subprocess import call

        _commands = {
            \"fedora\": \"dnf update -y\",
            \"debian\": \"apt-get upgrade -y\"
        }

        _dist = platform.dist()[0]
        _command = _commands[_dist]

        call(_command, shell=True)
    """)
