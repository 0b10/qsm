import sys
from invoke import run, task
from python_boilerplate.tasks import *


@task
def configure(ctx):
    """
    Instructions for preparing package for development.
    """

    run("%s -m pip install .[dev] -r requirements.txt" % sys.executable)


@task
def pep8(ctx):
    args = " ".join([
        "--recursive",
        "--in-place",
        "--max-line-length 120",
        "./src/"
    ])
    run("{} -m autopep8 {}".format(sys.executable, args))