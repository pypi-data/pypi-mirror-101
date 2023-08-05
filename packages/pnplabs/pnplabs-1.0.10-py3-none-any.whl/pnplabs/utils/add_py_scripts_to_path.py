import windowspathadder
import sys
from pathlib import Path
from pnplabs.utils.local_config import get_config, dump_config
import subprocess
import platform
import os


def verify_path_env_set(force=False):
    config = get_config()
    print(f"PATH: {os.environ['PATH']}")
    print(f"Platform: {platform.system()}")
    if "path_env_set" not in config or force:
        print("Missing pnplabs command shortcuts.")
        if platform.system() == "Windows":
            try:
                windows_runner()
            except Exception as e:
                print(f"Path set failed ({e})")
            config['path_env_set'] = {
                "done": True
            }
        elif platform.system() == "Darwin":
            try:
                macos_runner()
            except Exception as e:
                print(f"Path set failed ({e})")
            config['path_env_set'] = {
                "done": True
            }
    # else:
    #     print("path_env_set already ran")
    dump_config(config)


def macos_runner():
    python_scripts_dir = str(Path(sys.executable).parent)
    addition = f"""
    # Setting PATH for Python
    PATH="{python_scripts_dir}:${{PATH}}"
    export PATH
    """
    with open("~/.bash_profile", 'a') as fobj:
        fobj.write(addition)



def windows_runner():
    python_scripts_dir = str(Path(sys.executable).parent.joinpath("Scripts"))+'\\'
    permenant_set_path = f"setx PATH \"%PATH%;{python_scripts_dir}\\\""
    current_session_set_path = f"cmd /C \'set PATH=\"{python_scripts_dir};%PATH%\"\'"

    #print(f"Command: {list(permenant_set_path.split(' '))}")


    #result = subprocess.run(list(permenant_set_path.split(' ')), stdout=subprocess.PIPE)


    #print(f"{result.stdout.decode('utf-8')}", end='')

    # print(f"Command: {list(current_session_set_path.split(' '))}")
    # result = subprocess.run(list(current_session_set_path.split(' ')), stdout=subprocess.PIPE)
    # print(f"{result.stdout.decode('utf-8')}", end='')

    windowspathadder.add_windows_path(python_scripts_dir)

    print("Please restart your shell to call pnplabs directly (simply use the p/pnp/pnplabs commands)")



