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

**Important! save modes is not implemented right now; I am working on it. In the
meantime, you can just move files manually to substitute for save.**

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
USAGE: cpsm <mode> [args...]
 cpsm init  |  Initialize a directory
 cpsm n abbrev problem language  |  Create a new solution
 cpsm s abbrev problem language  |  Save an existing solution
 cpsm h  |  Display this help message
```

### Examples

Create a new cpp solution for uva 12345, in the uva/solving directory.

```
cpsm n uva 12345 cpp
```

Save that cpp file.

```
cpsm s uva 12345 cpp
```

## Uninstallation

Should you ever decide to uninstall cpsm :scream:, simply run:

```
pip uninstall cpsm
```

## TODO

CPSM is under (heavy) development. Here are some remaining tasks, in order of
priority:

1. Add documentation on config files to README
1. Add a CONTRIBUTING.md
1. Create the save mode
1. Avoid having errors in create mode just because an input file already exists
1. Add a demo video/gif
1. Add checks for the current directories in init mode (may be undesirable)
1. Enable compatibility with earlier Python (down to 3.4-3.5?), mainly by
   eliminating f-strings
1. Allow naming templates after something other than filetypes, to allow
   multiple templates for a given filetype
1. Make a website on Github Pages

## Credits

- [Kevin Wang](https://github.com/vitamintk), for encouraging me to push this to
  a full project
- [Tianjiao Huang](https://github.com/gitletH), for being a pre-pre-pre-beta tester and suggesting the use
  of Jinja
