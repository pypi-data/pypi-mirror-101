from appdirs import user_data_dir
import configparser
from os import makedirs
import os.path

APP_NAME = "pnplabs"
AUTHOR_NAME = "pnplabs"

USER_CONFIG_DIR_PATH = user_data_dir(APP_NAME, AUTHOR_NAME)
USER_CONFIG_PATH = os.path.join(USER_CONFIG_DIR_PATH, "config.ini")


def get_config():
    config = configparser.ConfigParser()
    if os.path.exists(USER_CONFIG_PATH):
        config.read(USER_CONFIG_PATH)
    return config


def get_config_as_str():
    if os.path.exists(USER_CONFIG_PATH):
        with open(USER_CONFIG_PATH) as fobj:
            return fobj.read()


def dump_config(config):
    os.makedirs(USER_CONFIG_DIR_PATH, exist_ok=True)
    with open(USER_CONFIG_PATH, 'w') as configfile:
        config.write(configfile)
