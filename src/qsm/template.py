from .run import run
from .remote import install as install_script, update as update_script


def update(target):
    run(command=update_script(), target=target, user="root")


def install(target, packages):
    run(command=install_script(packages), target=target, user="root")
