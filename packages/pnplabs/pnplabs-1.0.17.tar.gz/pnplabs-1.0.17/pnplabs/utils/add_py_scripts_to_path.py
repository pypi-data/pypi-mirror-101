import windowspathadder
import sys
from pathlib import Path
from pnplabs.utils.local_config import get_config, dump_config
import subprocess
import platform
import os


def get_real_executable_path():
    return os.path.realpath(sys.executable)


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


def get_macos_shell_cfg_file_paths():
    return [
        str(Path(os.getenv('HOME')).joinpath(".bash_profile")),
        str(Path(os.getenv('HOME')).joinpath(".bashrc")),
        str(Path(os.getenv('HOME')).joinpath(".zshrc")),
    ]


def macos_runner():
    print(f"B")
    python_scripts_dir = str(Path(get_real_executable_path()).parent)
    addition = f'\n# Setting PATH for Python\nPATH="{python_scripts_dir}:${{PATH}}"\nexport PATH\n'
    for cfg_file_path in get_macos_shell_cfg_file_paths():
        print(f"Adding {addition} to {cfg_file_path}")
        with open(cfg_file_path, 'a') as fobj:
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



