from qsm import config
from os.path import isfile, isdir
import os
import stat
import pytest


def _get_perms(path):
    return stat.S_IMODE(os.lstat(path).st_mode)


def test_config_tree_is_created(tmp_path):
    config_dir = tmp_path / ".qsm"
    plugins_dir = tmp_path / ".qsm" / "plugins"
    data_dir = tmp_path / ".qsm" / "data"
    config_file = tmp_path / ".qsm" / "qsm.conf"

    config.init(str(config_dir))

    assert isfile(str(config_file)), "the config file was not created"
    assert isdir(str(config_dir)), "the config directory was not created"
    assert isdir(str(plugins_dir)), "the plugins directory was not created"
    assert isdir(str(data_dir)), "the data directory was not created"


def test_config_file_is_created_when_dirs_already_exist(tmp_path):
    config_dir = str(tmp_path / ".qsm")
    config_file = str(tmp_path / ".qsm" / "qsm.conf")

    config.init(config_dir)
    assert isfile(config_file), "the config wasn't initially created"
    os.remove(config_file)
    assert not isfile(config_file), "the config file was not os.removed"
    config.init(config_dir)

    assert isfile(config_file), "the config file was not recreated"


def test_config_subdirs_are_recreated_when_config_dir_already_exists(tmp_path):
    config_dir = str(tmp_path / ".qsm")
    plugins_dir = str(tmp_path / ".qsm" / "plugins")
    data_dir = str(tmp_path / ".qsm" / "data")

    config.init(config_dir)
    os.rmdir(plugins_dir)
    os.rmdir(data_dir)
    assert not isdir(plugins_dir), "the plugins dir was not os.removed"
    assert not isdir(data_dir), "the data dir was not os.removed"
    config.init(config_dir)

    assert isdir(plugins_dir), "the plugins dir was not recreated"
    assert isdir(data_dir), "the data dir was not recreated"


def test_config_dir_permissions(tmp_path):
    config_dir = str(tmp_path / ".qsm")
    config_file = str(tmp_path / ".qsm" / "qsm.conf")
    plugins_dir = str(tmp_path / ".qsm" / "plugins")
    data_dir = str(tmp_path / ".qsm" / "data")

    config.init(config_dir)

    assert _get_perms(config_dir) == 0o750, "the config dir permissions are incorrect"
    assert _get_perms(plugins_dir) == 0o750, "the plugins dir permissions are incorrect"
    assert _get_perms(data_dir) == 0o750, "the data dir permissions are incorrect"
    assert _get_perms(config_file) == 0o640, "the config file permissions are incorrect"


def test_config_file_path_returned_from_init(tmp_path):
    config_dir = str(tmp_path / ".qsm")
    config_file = str(tmp_path / ".qsm" / "qsm.conf")

    assert config.init(config_dir) == config_file, "the config file path is incorrect"


def test_config_get_inits_config_dir(tmp_path):
    config_dir = str(tmp_path / ".qsm")

    config.get("data_dir", config_dir=config_dir)

    assert isdir(config_dir), "the config directory was not created"


def test__config__get__invalid_config_option(tmp_path):
    config_dir = str(tmp_path / ".qsm")

    with pytest.raises(config.QsmInvalidConfigOptionError):
        config.get("asjhdkjhd", config_dir=config_dir)


def test__config__get__all_valid_config_options(tmp_path):
    config_dir = str(tmp_path / ".qsm")
    data_dir = str(tmp_path / ".qsm" / "data")
    plugins_dir = str(tmp_path / ".qsm" / "plugins")

    assert config.get("data_dir", config_dir=config_dir) == data_dir, \
        "data dir dir doesn't match expected value"
    assert config.get("plugins_dir", config_dir=config_dir) == plugins_dir, \
        "plugins dir dir doesn't match expected value"
