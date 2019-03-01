# CPSM - Competitive Programming Solutions Manager

<!-- toc -->

- [Installation](#installation)
- [Usage](#usage)
  - [Examples](#examples)
- [TODO](#todo)

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

**Important! init and save modes are not implemented right now; I am working on
them. In the meantime, you can always copy the cpsm_config.py module I have here
and modify it yourself, instead of doing init. You can also just move file
manually to substitute for save.**

## Installation

To install, start by cloning this repo. Then, while in the repo, do:

```
pip install .
```

Now, you should be able to run the command `cpsm`.

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

CPSM is under development. Here are some remaining tasks:

- Create the init mode
- Create the save mode
- Add a CONTRIBUTING.md
