from os.path import join, expanduser, isfile
from os import makedirs, chmod
import json
import lib


def init(config_dir=join(expanduser("~"), ".qsm")):
    config_file = join(config_dir, "qsm.conf")
    pluging_dir = join(config_dir, "plugins")
    data_dir = join(config_dir, "data")

    makedirs(config_dir, exist_ok=True, mode=0o750)
    makedirs(pluging_dir, exist_ok=True, mode=0o750)
    makedirs(data_dir, exist_ok=True, mode=0o750)

    if not isfile(config_file):
        lib.print_header("creating a new config file")
        # true for dirs, let raise if is dir
        with open(config_file, "w") as f:
            json.dump({
                "data_dir": data_dir,
                "plugin_dir": pluging_dir
            }, f, indent=2, sort_keys=True)
            chmod(config_file, 0o640)
        lib.print_sub("config file created @ {}".format(config_file))

    return config_file


def config(option):
    with open(init(), "r") as f:
        return json.load(f)[option]
