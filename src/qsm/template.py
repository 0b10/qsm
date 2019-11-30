from .run import run
from .remote import install, update

def update(target):
    run(command=update(), target=target, user="root", shell="python -c")

def install(target, packages):
    run(command=install(packages), target=target, user="root", shell="python -c")