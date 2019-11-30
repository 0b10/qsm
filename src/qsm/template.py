from .run import run
from .remote import get

def update(target):
    run(command=get("update"), target=target, user="root", shell="bash")