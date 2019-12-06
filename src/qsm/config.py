from os.path import join, expanduser, isfile
from os import makedirs, chmod
import json

_CONFIG_DIR = join(expanduser("~"), ".qsm")
_CONFIG_FILE = join(_CONFIG_DIR, "qsm.conf")


def init():
    pluging_dir = join(_CONFIG_DIR, "plugins")
    data_dir = join(_CONFIG_DIR, "data")

    makedirs(_CONFIG_DIR, exist_ok=True, mode=0o750)
    makedirs(pluging_dir, exist_ok=True, mode=0o750)
    makedirs(data_dir, exist_ok=True, mode=0o750)

    if not isfile(_CONFIG_FILE):
        # true for dirs, let raise if is dir
        with open(_CONFIG_FILE, "w") as f:
            json.dump({
                "data_dir": data_dir,
                "plugin_dir": pluging_dir
            }, f, indent=2, sort_keys=True)
            chmod(_CONFIG_FILE, 0o640)


def config(option):
    init()
    with open(_CONFIG_FILE, "r") as f:
        return json.load(f)[option]
