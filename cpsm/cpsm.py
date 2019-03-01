"""Enables management of competitive programming solution files"""

import argparse
import json
import sys
import os
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


def init(args):
    """Initializes CPSM in the current directory"""
    pass


#
# Start/New mode
#


def retrieve_config() -> "module":
    """Retrieves template files from cpsm_templates.py"""
    try:
        import cpsm_config
        return cpsm_config
    except ModuleNotFoundError:
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

    replacements = {
        "$USERNAME": config.username,
        "$FULLNAME": config.fullname,
        "$PROBLEM_NAME": problem_name,
        "$NAME": config.abbreviations[args["abbrev"]]["name"],
    }

    # Create the appropriate files
    with code_file.open("w") as cfile:
        file_string = config.templates[args["language"]]
        for var, actual in replacements.items():
            file_string = file_string.replace(var, actual)
        cfile.write(file_string)
    with input_file.open("w") as ifile:
        pass  # Empty file

    # Launch editor
    os.system(f"{config.editor} {code_file} {input_file}")


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
