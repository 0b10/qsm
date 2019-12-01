from qsm.lib import run
from qsm.remote import install as install_script, update as update_script, remove as remove_script
from qsm.lib import print_header, print_sub, parse_packages


def update(target):
    print_header("updating {}".format(target))

    run(command=update_script(), target=target, user="root")

    print_sub("{} updated".format(target))


def install(target, packages):
    print_header("installing packages on {}".format(target))

    _packages = parse_packages(packages)
    run(command=install_script(_packages), target=target, user="root")

    print_sub("installed packages on {}".format(target))


def uninstall(target, packages):
    print_header("removing packages from {}".format(target))

    _packages = parse_packages(packages)
    run(command=remove_script(_packages), target=target, user="root")

    print_sub("removed packages from {}".format(target))
