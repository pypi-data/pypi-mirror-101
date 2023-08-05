from pnplabs.utils.firestore import get_db_client
from pnplabs.utils.local_config import get_config, dump_config
from pnplabs.utils.add_py_scripts_to_path import windows_runner

def get_api_key():
    config = get_config()
    return config['Connect']['api_key']


def execute(*args, **kwargs):
    # print(f"Executing connect command with {args}")
    api_key = args[0]

    config = get_config()
    config['Connect'] = {
        'api_key': api_key,
    }
    dump_config(config)

    # print(f"API key is {api_key}, getting client...")

    # Check the connection (without actually doing anything

    db_client = None
    try:
        db_client = get_db_client(api_key)
    except Exception as e:
        print("Connection failed")
    print(f"Connected!")
