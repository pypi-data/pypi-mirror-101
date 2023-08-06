# hdev

The CLI for the Hypothesis development environment.

Usage
-----

```
usage: hdev [-h] [-f CONFIG_PATH] {requirements} ...

positional arguments:
  {requirements}
    requirements  Compiles .txt requirements file based on the existing .in
                  files using pip-tools

optional arguments:
  -h, --help      show this help message and exit
  -f CONFIG_PATH  Path the the configuration file. Defaults to `.hdev.toml` in
                  the root of the project
```

To get hdev in your project you can either:

- Install from this repository:

```terminal
cd hdev
```

`python setup.py install --force`


- Install from pypi globally in your machine:


`pip install hdev`


- Add hdev as a dependency to the project you want to use it in:

Edit the project's dev.in and include `hdev` there.


Regardless of the installation method to use hdev just go to the root of the project
and create a `.hdev.toml` configuration there and just type `hdev` to use the tool.


Configuration 
-------------

hdev is configured within your project's pyproject.toml file with the following options:


```
[tool.hdev.requirements]
# Reformat .txt files to match pip-tools>5.5 formatting.
reformat = 1
# Order to process .in files based on their dependencies. Use relative paths from the the project's root.
order = []
```

You can choose to not use any configuration, in that case hdev provides sensible default for most H projects.


Hacking
-------

### Installing hdev in a development environment

#### You will need

* [Git](https://git-scm.com/)

* [pyenv](https://github.com/pyenv/pyenv)
  Follow the instructions in the pyenv README to install it.
  The Homebrew method works best on macOS.
  On Ubuntu follow the Basic GitHub Checkout method.

#### Clone the git repo

```terminal
git clone https://github.com/hypothesis/hdev.git
```

This will download the code into a `hdev` directory
in your current working directory. You need to be in the
`hdev` directory for the rest of the installation
process:

```terminal
cd hdev
```

#### Run the tests

```terminal
make test
```

**That's it!** You’ve finished setting up your hdev
development environment. Run `make help` to see all the commands that're
available for linting, code formatting, packaging, etc.

### Updating the Cookiecutter scaffolding

This project was created from the
https://github.com/hypothesis/h-cookiecutter-pypackage/ template.
If h-cookiecutter-pypackage itself has changed since this project was created, and
you want to update this project with the latest changes, you can "replay" the
cookiecutter over this project. Run:

```terminal
make template
```

**This will change the files in your working tree**, applying the latest
updates from the h-cookiecutter-pypackage template. Inspect and test the
changes, do any fixups that are needed, and then commit them to git and send a
pull request.

If you want `make template` to skip certain files, never changing them, add
these files to `"options.disable_replay"` in
[`.cookiecutter.json`](.cookiecutter.json) and commit that to git.

If you want `make template` to update a file that's listed in `disable_replay`
simply delete that file and then run `make template`, it'll recreate the file
for you.
