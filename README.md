# CPSM - Competitive Programming Solutions Manager

<!-- toc -->

- [Installation](#installation)
- [Usage](#usage)
  - [Examples](#examples)
- [Uninstallation](#uninstallation)
- [TODO](#todo)
- [Credits](#credits)

<!-- tocstop -->

CPSM is a tool for managing solutions to programming problems, particularly
competitive programming problems. It allows one to easily create and save new
solution files from templates.

CPSM assumes that, in a given directory, you have several directories holding
solutions to problems. Furthermore, within each directory, there should be a
`solving` directory holding problems that you are working on. Thus, the
structure should look something like this:

```
.
├── cpsm_config.py             <-- configuration file
├── website-1
│   ├── solution1.cpp
│   ├── solution2.py
│   ├── ...
│   └── solving
│       ├── solving1.cpp
│       └── solving2.py
└── website-2
    ├── solution1.cpp
    ├── solution2.py
    ├── ...
    └── solving
        ├── solving1.cpp
        └── solving2.py
```

Then, when you decide to save a file, it moves from the solving directory to its
main directory.

## Installation

CPSM requires Python 3.6 or later (compatibility with earlier versions may be
coming soon, however). To install, start by cloning this repo. Then, while in
the repo, do:

```
pip install -e .
```

Make sure you use the `-e` option! If you do not, Jinja will not be able to read
the templates. Now, you should be able to run the command `cpsm`.

In a directory where you want to create solutions, do

```
cpsm init
```

This will walk you through a few steps and eventually create a `cpsm_config.py`
file with your configuration. You can modify this `cpsm_config.py` file as you
wish, as long as you retain at least the original variables, as they are needed
by cpsm.

## Usage

```
USAGE: cpsm MODE [ARGS...]
  cpsm init | Initialize a directory for CPSM
  cpsm n abbrev problem language | Create a new solution (or open existing)
  cpsm s abbrev problem language | Save an existing solution
  cpsm h | Display the full help message
```

### Examples

Create a new cpp solution for the HackerRank problem "Journey to the Moon",
where the abbreviation for HackerRank is `hr` and the directory for it is
hackerrank.

```
cpsm n hr "Journey to the Moon" cpp
```

This creates a journey-to-the-moon.cpp and journey-to-the-moon.txt file in the
hackerrank/solving file and opens up an editor where you can work on the files.
_Note that if any of these files exist already, they will simply be opened._
Once you are done, you can move the files to the main hackerrank directory (i.e.
"save" it) with the following command.

```
cpsm s hr "Journey to the Moon" cpp
```

Note that you do not need quotes around your problem title if your problem title
has no spaces. For example, you can do `cpsm n uva 12345 cpp`.

## Uninstallation

Should you ever decide to uninstall cpsm :scream:, simply run:

```
pip uninstall cpsm
```

You may also want to remove your `cpsm_config.py` files if you are truly done
with CPSM.

## TODO

CPSM is under (heavy) development. Here are some remaining tasks, in order of
priority:

1. Add documentation on config files to README
1. Add a demo gif to README
1. Add NPM and use packages from it to automate linting, formatting, etc. for
   the repo.
1. Add a CONTRIBUTING.md
1. Add checks for the current directories in init mode (may be undesirable)
1. Check for existing input files in the main directory before creating a new
   one (and query the user to see if they would like to use that file).
1. Add a run mode to allow one to easily see output for a program and input
1. Enable compatibility with earlier Python (down to 3.4-3.5?), mainly by
   eliminating f-strings
1. Create a PyPI package
1. Allow naming templates after something other than filetypes, to allow
   multiple templates for a given filetype
1. Make a website on Github Pages - or a readthedocs page
1. Integrate testing? [shUnit](https://github.com/kward/shunit2)

## Credits

- [Kevin Wang](https://github.com/vitamintk), for encouraging me to push this to
  a full project
- [Tianjiao Huang](https://github.com/gitletH), for being a pre-pre-pre-beta tester and suggesting the use
  of Jinja
