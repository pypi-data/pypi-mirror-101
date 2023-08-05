import sys

from pnplabs.functions import connect, dynamic, instructions, verify_path, get_config
from pnplabs.utils.add_py_scripts_to_path import verify_path_env_set

FUNCTION_NAME_INDEX = 1

STATIC_FUNCTIONS = {
    "connect": connect.execute,
    "verify_path": verify_path.execute,
    "instructions": instructions.execute,
    "get_config": get_config.execute
}

DYNAMIC_FUNCTION = dynamic.execute


def parse(user_args=None):
    if not user_args:
        user_args = sys.argv

    verify_path_env_set()

    if len(user_args) <= 1:
        print("Sorry! Must call pnplabs with a command. For example, try: 'pnplabs instructions'")
        return

    required_function = user_args[FUNCTION_NAME_INDEX]
    function_args = user_args[FUNCTION_NAME_INDEX + 1:] if required_function in STATIC_FUNCTIONS else user_args[FUNCTION_NAME_INDEX:]

    # print(f"Required function: {required_function}")
    # print(f"Required args: {function_args}")

    STATIC_FUNCTIONS.get(required_function, DYNAMIC_FUNCTION)(*function_args)
