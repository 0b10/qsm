# MIT License
#
# Copyright (c) 2019 0b10
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from textwrap import dedent


# FIXME: platform.dist() has been moved to an external package in 3.7
def install(packages):
    return dedent("""\
        python3 -W ignore::DeprecationWarning -c \'
        import platform
        from subprocess import call

        _commands = {{
            \\"fedora\\": \\"dnf install -y {0}\\",
            \\"debian\\": \\"apt-get update && apt-get install -y {0}\\"
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
            \\"fedora\\": \\"dnf update -y\\",
            \\"debian\\": \\"apt-get update && apt-get upgrade -y\\"
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
            \\"fedora\\": \\"dnf remove -y {0}\\",
            \\"debian\\": \\"apt-get remove -y {0}\\"
        }}

        _dist = platform.dist()[0]
        _command = _commands[_dist]

        call(_command, shell=True)\'
    """.format(packages))

# >>> GIT >>>


def verify_repo_store(store_dir, user="user", group="user", mode=750):
    return dedent("""\
        python3 -c \'
        from os import makedirs
        from os.path import join, isdir
        from shutil import chown

        _store_dir = \\"{0}\\"
        _dist = join(_store_dir, "dist")
        _user = \\"{1}\\"
        _group = \\"{2}\\"
        _mode = 0o{3}

        if isdir(_store_dir):
            print("repo store exists @ {0}")
        else:
            print("repo store doesn\\'t exist, creating @ {0}")
            makedirs(_dist, _mode, exist_ok=True)
            chown(_store_dir, _user, _group)
            chown(_dist, _user, _group)\'
    """.format(store_dir, user, group, mode))


# this assumes that the repo store exists, it will fail otherwise. use verify_repo_store first
def git_pull(repo, repo_name, store_dir):
    return dedent("""\
        python3 -c \'
        from subprocess import call
        from os import chdir
        from os.path import join
        import sys

        _repo = \\"{0}\\"
        _store_dir = \\"{2}\\"
        _repo_name = \\"{1}\\"
        _local_repo = join(_store_dir, _repo_name)
        _clone = "git clone {0} {1}"

        try:
            chdir(_local_repo)
            call("git status 2>&1 > /dev/null", shell=True)
        except FileNotFoundError:
            print("repo doesn't exist: {1}")
            chdir(_store_dir)
            sys.exit(call(_clone, shell=True))

        print("pulling updates for: {1}")
        chdir(_local_repo)
        sys.exit(call("git pull", shell=True))\'
    """.format(repo, repo_name, store_dir))
