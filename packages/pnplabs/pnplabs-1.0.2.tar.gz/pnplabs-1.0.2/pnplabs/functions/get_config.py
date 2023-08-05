from pnplabs.utils.local_config import get_config, dump_config, USER_CONFIG_PATH


def execute(*args, **kwargs):
    print(f"Here's pnplabs config from path {USER_CONFIG_PATH} :")
    print(get_config())
