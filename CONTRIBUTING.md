# Contributing to CPSM

Thank you for your interest in contributing to CPSM!

<!-- toc -->

- [Getting Started](#getting-started)
- [Project Organization](#project-organization)
- [Making Changes](#making-changes)
  - [Example Workflows](#example-workflows)
    - [Adding a Config Variable to cpsm_config.py](#adding-a-config-variable-to-cpsm_configpy)
    - [Adding a new Mode](#adding-a-new-mode)
- [Resources](#resources)

<!-- tocstop -->

## Getting Started

1. Make sure you have a [GitHub account](https://github.com/signup/free).
1. [Fork](https://help.github.com/articles/fork-a-repo/) this repository on GitHub.
1. On your local machine,
   [clone](https://help.github.com/articles/cloning-a-repository/) your fork of
   the repository.
1. Once you have cloned the repo, create a virtual environment (e.g. with
   `virtualenv` or python's `venv` module) and run:

   ```
   pip install -e .
   ```

   to install cpsm. Then, run

   ```
   npm install
   ```

   to install several development tools. These use
   [husky](https://github.com/typicode/husky) and
   [lint-staged](https://github.com/okonet/lint-staged) to automatically run
   various tools on files that are being committed. (See
   [here](https://www.39digits.com/automatically-format-your-javascript-commits-using-prettier-and-husky/)
   for more info).

## Project Organization

```
.
├── bin               // executables
├── cpsm              // main project directory
│   └── templates     // Jinja templates
└── docs              // material related to documentation
```

## Making Changes

1. Add some really awesome code to your local fork. It's usually a [good
   idea](http://blog.jasonmeridth.com/posts/do-not-issue-pull-requests-from-your-master-branch/)
   to make changes on a
   [branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/)
   with the branch name relating to the feature you are going to add.
1. When you commit your code, husky will automatically run various formatters on
   the code.
1. When you are ready for others to examine and comment on your new feature,
   navigate to your fork of cpsm on GitHub and open a [pull
   request](https://help.github.com/articles/using-pull-requests/) (PR). Note that
   after you launch a PR from one of your fork's branches, all
   subsequent commits to that branch will be added to the open pull request
   automatically.
1. Once you mark the "Ready to go" box in your Pull Request message, your code
   will be reviewed and commented on, and (hopefully) eventually merged!

### Example Workflows

#### Adding a Config Variable to cpsm_config.py

1. Add the variable to `cpsm/templates/cpsm_config_template.j2`
1. Add the variable to `get_init_options` in `cpsm.py`
1. Add logic, in a mode such as `save` or `start`, that makes use of the config
   variable.
1. Add the variable to the `cpsm_config.py` example under `Customization` in
   README, and add info about it elsewhere if applicable.

#### Adding a new Mode

1. Decide what command line arguments are needed for the mode.
1. Add the mode, its command line arguments, and help message to `MODES` in
   `cpsm.py`
1. Document the mode in README, particularly under the `Examples` and `Usage`
   section.
1. Decide what config variables (if any) are needed for the mode, and add them
   using the instructions [above](#adding-a-config-variable-to-cpsm_configpy)
1. Add a function to `cpsm.py` that takes in `args` and then figures out what to
   do for the new mode.
1. Add the mode name and the function to the `mode_functions` dictionary in
   `main` in `cpsm.py`.

## Resources

Below are some useful resources related to the creation of CPSM:

- [Quick Primer on Jinja](http://zetcode.com/python/jinja/)
- [Jinja documentation](http://jinja.pocoo.org/docs/2.10/)
- [Python Importlib](https://www.blog.pythonlibrary.org/2016/05/27/python-201-an-intro-to-importlib/)
- [Publishing a PyPI Package](https://realpython.com/pypi-publish-python-package/)
