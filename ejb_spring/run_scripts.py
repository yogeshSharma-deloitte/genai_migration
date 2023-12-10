import os
import platform
import subprocess
import sys

def run_shell_script(script_path, *args):
    try:
        if platform.system() == "Windows":
            subprocess.call([script_path] + list(args), shell=True)
        else:
            subprocess.call([script_path] + list(args))
    except Exception as e:
        print(f"Error running {script_path}: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_scripts.py <script_name> [arg1] [arg2] [arg3]")
        sys.exit(1)

    script_name = sys.argv[1]
    script_args = sys.argv[2:]

    if platform.system() != "Windows":
        script_name = script_name + ".sh"
        run_shell_script(script_name, *script_args)
    elif platform.system() == "Windows":
        script_name = script_name + ".bat"
        run_shell_script(script_name, *script_args)
    else:
        print(f"Unsupported script type or platform: {script_name}")
        sys.exit(1)

if __name__ == "__main__":
    main()
