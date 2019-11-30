from .run import run_remote
from .remote import get

def update(target):
    run_remote(command=get("update"), target=target, user="root")

def install(target, packages):
    run_remote(command=get("install"), target=target, args=packages, user="root")