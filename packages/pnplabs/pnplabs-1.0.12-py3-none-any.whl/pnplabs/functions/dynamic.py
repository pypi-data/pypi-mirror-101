from pnplabs.functions.connect import get_api_key
from pnplabs.utils.firestore import get_db_client
from pnplabs.utils.commands import get_commands
import subprocess


def execute(*args, **kwargs):
    # print(f"Executing dynamic command with {args}")

    dynamic_function_name = args[0]

    api_key = get_api_key()
    if not api_key:
        print("Cannot run dynamic functions before connection. Please connect first.")
        return

    db_client = get_db_client(api_key)
    commands = get_commands(db_client, api_key)
    for command in commands:
        if command["name"] == dynamic_function_name:
            #print("found cloud command!")
            result = subprocess.run(list(command["command"].split(' ')), stdout=subprocess.PIPE)
            print(f"{result.stdout.decode('utf-8')}", end='')
            return
    print("Command not found!")
