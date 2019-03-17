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
    ("r", {
        "args": ["abbrev", "problem", "filetype"],
        "help": "Run a solution",
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


def problem_to_filename(problem_name: str) -> str:
    """Converts a problem name to a filename"""
    return problem_name.lower().replace(' ', '-')


def solving_dir_path(maindir: str) -> Path:
    """
    Create a path to the solving directory in a given directory, and exit if it
    does not exist.
    """
    solvingdir = Path(maindir) / "solving"
    error_and_exit(f"{solvingdir} does not exist", not solvingdir.exists())
    return solvingdir


def create_filepaths(config: "module", abbrev: str, problem_name: str,
                     code_filetype: str) -> (Path, Path):
    """
    Creates paths for the code and input file for the solutions. Prints an
    error and exits if the abbreviation is not in the config, or if the
    directory for the given abbreviation does not exist.
    """
    filename = problem_to_filename(problem_name)

    error_and_exit(f"No config for the abbreviation: {abbrev}",
                   abbrev not in config.abbreviations)
    directory = solving_dir_path(config.abbreviations[abbrev]["dir"])
    code_file = directory / f"{filename}.{code_filetype}"
    input_file = directory / f"{filename}.txt"

    return (code_file, input_file)


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
        response = input(f"{msg} {'[Yes/no]' if default else '[yes/No]'}: "
                         ).strip().lower()
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

    print()
    options["git_init"] = read_yes_no(
        "Should this directory be initialized as a git repo?")
    if options["git_init"]:
        options["save_code_to_git"] = read_yes_no(
            "Should code files be added and committed to the git repo?")
        options["save_input_to_git"] = read_yes_no(
            "Should input files be added and committed to the git repo?")
    else:
        options["save_code_to_git"] = False
        options["save_input_to_git"] = False

    return options


def init(args):
    """Initializes CPSM in the current directory"""
    env = jinja2.Environment(loader=jinja2.PackageLoader("cpsm", "templates"))
    template = env.get_template("cpsm_config_template.j2")
    check_conf_exists()
    options = get_init_options()

    with Path("cpsm_config.py").open("w") as conf_file:
        conf_file.write(template.render(options))

    if options["git_init"]: os.system("git init")

    print("Success! CPSM has been configured in this directory. To change "
          "configurations, particularly your templates, edit the "
          "cpsm_config.py file at any time.")


#
# Start/New mode
#


def start(args):
    """Starts a solution file and input"""
    config = retrieve_config()
    error_and_exit(f"No config for template: {args['template']}",
                   args["template"] not in config.templates)
    code_file, input_file = create_filepaths(
        config, args["abbrev"], args["problem"],
        config.templates[args["template"]]["filetype"])
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
# Run mode
#


def run(args):
    """Runs a solution file"""
    config = retrieve_config()
    error_and_exit(f"No config for running filetype {args['filetype']}",
                   args["filetype"] not in config.run_commands)
    problem_name = str(
        solving_dir_path(config.abbreviations[args["abbrev"]]["dir"]) /
        problem_to_filename(args["problem"]))
    for cmd in config.run_commands[args["filetype"]]:
        os.system(jinja2.Template(cmd).render(problem_name=problem_name))


#
# Save mode
#


def save_with_check(file: Path, save_to_git: bool):
    """
    Saves the file by moving it to the main directory. Checks if the file in the
    main directory already exists and provides a prompt to the user if so. Also
    checks if the file passed in does not exist at all.
    """
    error_and_exit(f"{file} does not exist!", not file.exists())
    new_file = file.parent.parent / file.name
    if not new_file.exists() or (new_file.exists() and read_yes_no(
            f"{new_file} already exists. Overwrite?", False)):
        file.rename(new_file)
        if save_to_git:
            os.system(f"git add {new_file}")
            os.system(f"git commit -m \"Add {new_file}\"")
        print(f"Saved {file} to {new_file}")
    else:
        print(f"Ok. Leaving {file} as is.")


def save(args):
    """Saves a solution file"""
    config = retrieve_config()
    code_file, input_file = create_filepaths(config, args["abbrev"],
                                             args["problem"], args["filetype"])
    save_with_check(code_file, config.save_code_to_git)
    save_with_check(input_file, config.save_input_to_git)


#
# Main
#


def main():
    args = parse_commandline_flags()
    mode_functions = {"init": init, "n": start, "r": run, "s": save}
    mode_functions[args["mode"]](args)


if __name__ == "__main__":
    main()
