# Contributing to CPSM

Thank you for your interest in contributing to CPSM!

<!-- toc -->

- [Getting Started](#getting-started)
- [Project Organization](#project-organization)
- [Making Changes](#making-changes)
- [Resources](#resources)

<!-- tocstop -->

## Getting Started

1. Make sure you have a [GitHub account](https://github.com/signup/free).
1. [Fork](https://help.github.com/articles/fork-a-repo/) this repository on GitHub.
1. On your local machine,
   [clone](https://help.github.com/articles/cloning-a-repository/) your fork of
   the repository.
1. Once you have cloned the repo, run:

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
1. Your code will be reviewed and commented on, and (hopefully) eventually
   merged!

## Resources

Below are some useful resources related to the tools and libraries used to build
CPSM:

- [Quick Primer on Jinja](http://zetcode.com/python/jinja/)
- [Jinja documentation](http://jinja.pocoo.org/docs/2.10/)
- [Python Importlib](https://www.blog.pythonlibrary.org/2016/05/27/python-201-an-intro-to-importlib/)
