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
from qsm.lib import run
from qsm.remote import install as install_script, update as update_script, remove as remove_script
from qsm.lib import print_header, print_sub, parse_packages


def update(target):
    print_header("updating {}".format(target))

    run(command=update_script(), target=target, user="root")

    print_sub("{} update finished".format(target))


def install(target, packages):
    print_header("installing packages on {}".format(target))

    _packages = parse_packages(packages)
    run(command=install_script(_packages), target=target, user="root")

    print_sub("{} package installation finished".format(target))


def uninstall(target, packages):
    print_header("removing packages from {}".format(target))

    _packages = parse_packages(packages)
    run(command=remove_script(_packages), target=target, user="root")

    print_sub("{} package uninstallation finished".format(target))
