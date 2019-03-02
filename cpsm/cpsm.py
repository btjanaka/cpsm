"""Enables management of competitive programming solution files"""

import importlib.util
import jinja2
import json
import os
import sys
from pathlib import Path

#
# Command line
#

USAGE = """\
USAGE: cpsm <mode> [args...]
 cpsm init  |  Initialize a directory
 cpsm n abbrev problem language  |  Create a new solution
 cpsm s abbrev problem language  |  Save an existing solution
 cpsm h  |  Display this help message
"""


def usage():
    print(USAGE, end='')
    sys.exit(1)


def parse_commandline_flags() -> {str: "argument value"}:
    args = {"init": False, "n": False, "s": False}

    if len(sys.argv) == 1:
        usage()
    elif sys.argv[1] == "h":
        usage()
    elif sys.argv[1] == "init":
        if len(sys.argv) != 2: usage()
        args["init"] = True
    elif sys.argv[1] == "n" or sys.argv[1] == "s":
        if len(sys.argv) != 5: usage()
        args[sys.argv[1]] = True
        args["abbrev"] = sys.argv[2]
        args["problem"] = sys.argv[3]
        args["language"] = sys.argv[4]
    else:
        usage()

    return args


#
# Misc utility
#


def error_and_exit(msg: str):
    """Prints an error and exits"""
    print(msg, file=sys.stderr)
    sys.exit(1)


#
# Initialization mode
#


def check_conf_exists():
    """Checks if a conf file already exists in the current directory."""
    conf_file = Path(".") / "cpsm_config.py"
    if conf_file.exists():
        error_and_exit("Configuration file already exists!")


def read_yes_no(msg: str) -> bool:
    """
    Reads in a yes/no response from the user and returns a bool indicating
    the response. The msg will be displayed as |$msg [Yes/no]: |
    """
    while True:
        response = input(f"{msg} [Yes/no]: ").strip().lower()
        if response in ("", "yes", "y"):
            return True
        elif response in ("no", "n"):
            return False
        print("Sorry, I don't understand that")


def read_string(msg: str, default: str) -> str:
    """
    Reads in a string from the user with the given message and default value.
    The msg is displayed as |$msg [$default]: |
    """
    response = input(f"{msg} [{default}]: ").strip()
    return default if response == "" else response


def get_init_options() -> dict:
    """Read in options for initializing cpsm"""

    # Various options to load into the template
    options = {}
    options["username"] = read_string("What is your username (not full name)?",
                                      "anonymous")
    options["fullname"] = read_string("What is your full name?", "anonymous")
    options["editor"] = read_string(
        "What editor command should be used to open your files?", "vim -p")
    options["open_input"] = "True" if \
        read_yes_no("Should CPSM open input files whenever it opens code "
                    "files?") else "False"

    # abbrevs is a list of dictionaries with the keys "abbrev",
    # "name", and "dir"
    print()
    print("We will now set up your abbreviations. These abbreviations are "
          "used to identify directories in here, as well as the names of "
          "the websites/competitions/etc associated with them.")
    options["abbrevs"] = []
    while read_yes_no("Would you like to add an abbreviation?"):
        cur_abbrev = {}
        cur_abbrev["abbrev"] = read_string(
            "What is this abbreviation? (make it short; 2-3 letters)", "abc")
        cur_abbrev["name"] = read_string(
            ("What is the website/competition/etc associated with this "
             "abbreviation?"), "MySite")
        cur_abbrev["dir"] = read_string(
            "What is the directory for this abbreviation?", "dir")
        options["abbrevs"].append(cur_abbrev)

    return options


def init(args):
    """Initializes CPSM in the current directory"""
    env = jinja2.Environment(loader=jinja2.PackageLoader("cpsm", "templates"))
    template = env.get_template("cpsm_config_template.j2")
    check_conf_exists()
    options = get_init_options()

    with (Path(".") / "cpsm_config.py").open("w") as conf_file:
        conf_file.write(template.render(options))

    print("Success! CPSM has been configured in this directory. To change "
          "configurations, particularly your templates, edit the "
          "cpsm_config.py file at any time.")


#
# Start/New mode
#


def retrieve_config() -> "module":
    """Retrieves configuration info"""
    try:
        module_spec = importlib.util.spec_from_file_location(
            "cpsm_config", "cpsm_config.py")
        configs = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(configs)
        return configs
    except FileNotFoundError:
        error_and_exit("ERROR: you need a cpsm_config.py file!")


def check_start_cmdline_errors(config, args):
    """Checks for errors in the arguments passed by the user for start mode"""
    if args["abbrev"] not in config.abbreviations:
        error_and_exit(
            f"ERROR: No config for the abbreviation: {args['abbrev']}")
    if args["language"] not in config.templates:
        error_and_exit(
            f"ERROR: No config for filetype/language: {args['language']}")


def create_files(config, args) -> (Path, Path):
    """Creates a code and input file for the solutions"""
    filename = args["problem"].lower().replace(' ', '-')

    directory = Path(".") / config.abbreviations[
        args["abbrev"]]["dir"] / "solving"
    if not directory.exists():
        error_and_exit(f"ERROR: {directory} does not exist")

    code_file = directory / f"{filename}.{args['language']}"
    input_file = directory / f"{filename}.txt"
    if code_file.exists() or input_file.exists():
        error_and_exit(f"Error: Files already exist!")

    return (code_file, input_file)


def start(args):
    """Starts a solution file and input"""
    config = retrieve_config()
    check_start_cmdline_errors(config, args)
    code_file, input_file = create_files(config, args)
    problem_name = args["problem"].lower().replace(' ', '-')

    config.mappings["name"] = config.abbreviations[args["abbrev"]]["name"]
    config.mappings["problem_name"] = problem_name

    # Create the appropriate files
    with code_file.open("w") as cfile:
        template = jinja2.Template(config.templates[args["language"]])
        cfile.write(template.render(config.mappings))
    with input_file.open("w") as ifile:
        pass  # Empty file

    # Launch editor
    if config.open_input:
        os.system(f"{config.editor} {code_file} {input_file}")
    else:
        os.system(f"{config.editor} {code_file}")


#
# Save mode
#


def save(args):
    """Saves a solution file"""
    pass


#
# Main
#


def main():
    args = parse_commandline_flags()
    if args["init"]:
        init(args)
    elif args["s"]:
        save(args)
    else:
        start(args)


if __name__ == "__main__":
    main()
