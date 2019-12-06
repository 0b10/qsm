from os.path import join, expanduser, isfile
from os import makedirs, chmod
import json
from qsm import lib


class QsmInvalidConfigOptionError(Exception):
    """
    Raised when an invalid config option is used.
    """
    pass


def init(config_dir=join(expanduser("~"), ".qsm")):
    config_file = join(config_dir, "qsm.conf")
    plugins_dir = join(config_dir, "plugins")
    data_dir = join(config_dir, "data")

    makedirs(config_dir, exist_ok=True, mode=0o750)
    makedirs(plugins_dir, exist_ok=True, mode=0o750)
    makedirs(data_dir, exist_ok=True, mode=0o750)

    if not isfile(config_file):
        lib.print_header("creating a new config file")
        # true for dirs, let raise if is dir
        with open(config_file, "w") as f:
            json.dump({
                "data_dir": data_dir,
                "plugins_dir": plugins_dir
            }, f, indent=2, sort_keys=True)
            chmod(config_file, 0o640)
        lib.print_sub("config file created @ {}".format(config_file))

    return config_file


def get(option, config_dir=join(expanduser("~"), ".qsm")):
    with open(init(config_dir), "r") as f:
        try:
            return json.load(f)[option]
        except KeyError:
            raise QsmInvalidConfigOptionError("invalid config option requested: {}".format(option))
