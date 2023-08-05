from appdirs import user_data_dir
import configparser
from os import makedirs
import os.path

APP_NAME = "pnplabs"
AUTHOR_NAME = "pnplabs"

USER_COMMANDS_DIR_PATH = os.path.join(user_data_dir(APP_NAME, AUTHOR_NAME), "commands")


def add_commands_dir_to_path():
    pass


def add_script_to_commands_dir():
    pass


def add_command(command):
    os.makedirs(USER_COMMANDS_DIR_PATH, exist_ok=True)
    command_path = os.path.join(USER_COMMANDS_DIR_PATH, command["name"])
    with open(command_path, 'w') as commandfile:
        commandfile.write("test")
