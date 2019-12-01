from .run import run
from .remote import install as install_script, update as update_script


def update(target):
    run(command=update_script(), target=target, user="root")


def install(target, packages):
    _packages = ' '.join(packages) if type(packages) is list else packages
    run(command=install_script(_packages), target=target, user="root")
