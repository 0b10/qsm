from textwrap import dedent


# FIXME: platform.dist() has been moved to an external package in 3.7
def install(packages):
    return dedent("""\
        python3 -W ignore::DeprecationWarning -c \'
        import platform
        from subprocess import call

        _commands = {{
            \"fedora\": \"dnf install -y {0}\",
            \"debian\": \"apt-get update && apt-get install -y {0}\"
        }}

        _dist = platform.dist()[0]
        _command = _commands[_dist]

        call(_command, shell=True)\'
    """.format(packages))


# FIXME: platform.dist() has been moved to an external package in 3.7
def update():
    return dedent("""\
        python3 -W ignore::DeprecationWarning -c \'
        import platform
        from subprocess import call

        _commands = {
            \"fedora\": \"dnf update -y\",
            \"debian\": \"apt-get update && apt-get upgrade -y\"
        }

        _dist = platform.dist()[0]
        _command = _commands[_dist]

        call(_command, shell=True)\'
    """)


# FIXME: platform.dist() has been moved to an external package in 3.7
def remove(packages):
    return dedent("""\
        python3 -W ignore::DeprecationWarning -c \'
        import platform
        from subprocess import call

        _commands = {{
            \"fedora\": \"dnf remove -y {0}\",
            \"debian\": \"apt-get remove -y {0}\"
        }}

        _dist = platform.dist()[0]
        _command = _commands[_dist]

        call(_command, shell=True)\'
    """.format(packages))
