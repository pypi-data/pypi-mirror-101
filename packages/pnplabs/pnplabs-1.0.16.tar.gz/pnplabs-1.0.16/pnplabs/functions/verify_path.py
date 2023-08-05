from pnplabs.utils.add_py_scripts_to_path import verify_path_env_set


def execute(*args, **kwargs):
    print(f"Verify path env set")
    verify_path_env_set(force=True)
