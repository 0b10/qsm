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

# >>> GIT >>>


def verify_repo_store(store_dir="/rw/repo_store", user="user", group="user", mode=750):
    return dedent("""\
        python3 -W ignore::DeprecationWarning -c \'
        from os import makedirs
        from os.path import join, isdir
        from shutil import chown

        _store_dir = \"{0}\"
        _dist = join(_store_dir, "dist")
        _user = \"{1}\"
        _group = \"{2}\"
        _mode = 0o{3}\

        if isdir(_store_dir):
            print("repo store exists @ {0}")
        else:
            print("repo store doesn\\'t exist, creating @ {0}")
            makedirs(_dist, _mode, exist_ok=True)
            chown(_store_dir, _user, _group)
            chown(_dist, _user, _group)\'
    """.format(store_dir, user, group, mode))
