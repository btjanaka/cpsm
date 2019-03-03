"""Enables management of competitive programming solution files"""

import importlib.util
import jinja2
import json
import os
import sys
from pathlib import Path
from collections import OrderedDict

#
# Command line
#

# Mapping of mode names to:
# - "args": list of arguments that the mode takes, in the order they must appear
#   on the command line
# - "help": help message for that mode
# OrderedDict used to enforce ordering when printing usage messages.
MODES = OrderedDict([
    ("init", {
        "args": [],
        "help": "Initialize a directory for CPSM",
    }),
    ("n", {
        "args": ["abbrev", "problem", "template"],
        "help": "Create a new solution (or open existing)",
    }),
    ("s", {
        "args": ["abbrev", "problem", "filetype"],
        "help": "Save an existing solution",
    }),
    ("h", {
        "args": [],
        "help": "Display this help message",
    }),
])


def print_mode(mode: str):
    if mode in MODES:
        print(f"  cpsm {mode} {' '.join(MODES[mode]['args'])}"
              f"{'' if len(MODES[mode]['args']) == 0 else ' '}"
              f"| {MODES[mode]['help']}")
    else:
        print("Invalid mode!")


def usage(mode=None):
    """
    Prints usage message for given mode (all modes if mode is None) and exits.
    """
    print("USAGE: cpsm MODE [ARGS...]")
    if mode is not None:
        print_mode(mode)
    else:
        for m in MODES:
            print_mode(m)
    sys.exit(0)


def parse_commandline_flags() -> {str: "argument value"}:
    """
    Parses all flags from the command line and returns the args. args will only
    contain the values of the arguments for the given mode; this mode is stored
    in args["mode"]
    """
    if len(sys.argv) == 1: usage()

    # Retrieve mode
    mode = sys.argv[1]
    if mode not in MODES or mode == "h": usage()

    # Check for correct number of arguments - 2 are for "cpsm MODE"
    if len(sys.argv) != 2 + len(MODES[mode]["args"]): usage(mode)

    # Fill up arguments
    args = {}
    for i in range(len(MODES[mode]["args"])):
        args[MODES[mode]["args"][i]] = sys.argv[i + 2]

    args["mode"] = mode
    return args


#
# Misc utility
#


def error_and_exit(msg: str, condition=True):
    """Prints an error and exits if the given condition is true"""
    if condition:
        print(f"ERROR: {msg}")
        sys.exit(1)


#
# Initialization mode
#


def check_conf_exists():
    """Checks if a conf file already exists in the current directory."""
    conf_file = Path("cpsm_config.py")
    error_and_exit("Configuration file already exists!", conf_file.exists())


def read_yes_no(msg: str, default=True) -> bool:
    """
    Reads in a yes/no response from the user and returns a bool indicating
    the response. The msg will be displayed as |$msg [Yes/no]: |. |default| is
    the default between yes/no.
    """
    while True:
        response = input(
            f"{msg} {'[Yes/no]' if default else '[yes/No]'}: ").strip().lower()
        if response == "":
            return default
        elif response in ("yes", "y"):
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

    with Path("cpsm_config.py").open("w") as conf_file:
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
        error_and_exit("You need a cpsm_config.py file!")


def create_filepaths(config, args, code_filetype) -> (Path, Path):
    """Creates paths for the code and input file for the solutions"""
    filename = args["problem"].lower().replace(' ', '-')

    error_and_exit(f"No config for the abbreviation: {args['abbrev']}",
                   args["abbrev"] not in config.abbreviations)
    directory = Path(config.abbreviations[args["abbrev"]]["dir"]) / "solving"
    error_and_exit(f"{directory} does not exist", not directory.exists())

    code_file = directory / f"{filename}.{code_filetype}"
    input_file = directory / f"{filename}.txt"

    return (code_file, input_file)


def start(args):
    """Starts a solution file and input"""
    config = retrieve_config()
    error_and_exit(f"No config for template: {args['template']}",
                   args["template"] not in config.templates)
    code_file, input_file = create_filepaths(
        config, args, config.templates[args["template"]]["filetype"])
    problem_name = args["problem"].lower().replace(' ', '-')

    config.mappings["name"] = config.abbreviations[args["abbrev"]]["name"]
    config.mappings["problem_name"] = problem_name

    # Create the appropriate files (if necessary)
    if not code_file.exists():
        with code_file.open("w") as cfile:
            template = jinja2.Template(
                config.templates[args["template"]]["code"])
            cfile.write(template.render(config.mappings))
    if not input_file.exists():
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


def save_with_check(file: Path):
    """
    Saves the file by moving it to the main directory, but also checks if it
    already exists and provides a prompt to the user if so.
    """
    error_and_exit(f"{file} does not exist!", not file.exists())
    new_file = file.parent.parent / file.name
    if not new_file.exists() or (new_file.exists() and read_yes_no(
            f"{new_file} already exists. Overwrite?", False)):
        file.rename(new_file)
        print(f"Saved {file} to {new_file}")
    else:
        print(f"Ok. Leaving {file} as is.")


def save(args):
    """Saves a solution file"""
    config = retrieve_config()
    code_file, input_file = create_filepaths(config, args, args["filetype"])
    save_with_check(code_file)
    save_with_check(input_file)


#
# Main
#


def main():
    args = parse_commandline_flags()
    run = {"init": init, "n": start, "s": save}
    run[args["mode"]](args)


if __name__ == "__main__":
    main()
