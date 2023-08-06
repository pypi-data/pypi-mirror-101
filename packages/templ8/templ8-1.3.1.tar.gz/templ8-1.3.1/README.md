# templ8

A powerful, extensible templating engine.

## Status

| Source     | Shields                                                                                                                         |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Project    | ![release][release_shield] ![license][license_shield] ![lines][lines_shield] ![languages][languages_shield]                     |
| Health     | ![codacy][codacy_shield] ![readthedocs][readthedocs_shield] ![travis][travis_shield] ![codacy_coverage][codacy_coverage_shield] |
| Repository | ![issues][issues_shield] ![issues_closed][issues_closed_shield] ![pulls][pulls_shield] ![pulls_closed][pulls_closed_shield]     |
| Publishers | ![pypi][pypi_shield] ![python_versions][python_versions_shield] ![pypi_downloads][pypi_downloads_shield]                        |
| Activity   | ![contributors][contributors_shield] ![monthly_commits][monthly_commits_shield] ![last_commit][last_commit_shield]              |

## Installing

```bash
pip install templ8
```

## Usage

```bash
usage: templ8 [-h] [-d] [-v] [-c] [-s] input

positional arguments:
  input          Input file path

optional arguments:
  -h, --help     Show this help message and exit
  -d, --dry-run  Don't generate anything
  -v, --verbose  Output verbose logs
  -c, --schema   Print schema
  -s, --silent   Don't output any logs
```

### Features

The engine can:

- Parse Jinja templates.
- Copy static files.
- Set default values for render context.
- Dynamically rename folders after generation.
- Run initialization scripts.

You can specify:

- Files to include.
- Render context values.
- Protected files not to touch.
- Collection sources to search.
- Loader paths for jinja include tags.
- Whether to clear top level files.
- To allow logical input sub-grouping.

### Example

**`.template.yml`**:

```yml
output_dir: .

clear_top_level: true
logical_grouping: true

collections:
  - common
  - python

protected:
  - .gitignore
  - .cspell.json
  - .travis.yml

loader_paths:
  - docs

render_context:
  project:
    project_name: templ8
    verbose_name: templ8
    description: A powerful, extensible templating engine.
    repository: https://github.com/JoelLefkowitz/templ8
    usage: usage.md
    codacy_id: f407d8c4db8c4b83877bca0543aba744

  author:
    author: Joel Lefkowitz
    author_email: joellefkowitz@hotmail.com
    author_github_handle: joellefkowitz

  package:
    is_pypi_package: true
    package_name: templ8

    console_scripts:
      - "templ8 = templ8.__main__:main"

    install_requires:
      - art
      - dataclasses
      - deepmerge
      - jinja2schema
      - pyyaml
      - simple_chalk
      - simple_pipes
      - typing-extensions
      - walkmate

  portfolio:
    is_portfolio: true
    status_level: 4
```

```bash
Clearing top level files
> Deleting Gruntfile.js
> Deleting LICENSE.md
> Deleting .pylintrc
> Deleting .mypy.ini
> Leaving .cspell.json unchanged
> Deleting CHANGELOG.md
> Deleting .coverage
> Deleting .bandit
> Deleting .bumpversion.cfg
> Deleting .quickdocs.yml
> Deleting .readthedocs.yml
> Deleting .prettierignore
> Deleting README.md
> Deleting setup.py
> Leaving .gitignore unchanged
> Deleting package-lock.json
> Deleting package.json
> Deleting CONTRIBUTING.md
> Deleting tox.ini
> Deleting setup.cfg
> Deleting .remarkrc
> Deleting coverage.xml
> Deleting .prettier.yml
> Leaving .travis.yml unchanged
> Deleting .remarkignore
> Leaving .template.yml unchanged

Generating common collection
Templates: 4
Static files: 12
Dynamic folders: 0
Initialization scripts: 0
> Templating .quickdocs.yml
> Templating .bumpversion.cfg
> Templating LICENSE.md
> Templating README.md
> Copying Gruntfile.js
> Leaving .cspell.json unchanged
> Copying CHANGELOG.md
> Copying .readthedocs.yml
> Copying .prettierignore
> Leaving .gitignore unchanged
> Copying package.json
> Copying CONTRIBUTING.md
> Copying .remarkrc
> Copying .prettier.yml
> Leaving .travis.yml unchanged
> Copying .remarkignore

Generating python collection
Templates: 5
Static files: 5
Dynamic folders: 1
Initialization scripts: 1
> Templating setup.cfg
> Templating setup.py
> Templating tox.ini
> Leaving .travis.yml unchanged
> Templating Gruntfile.js
> Copying .pylintrc
> Copying .mypy.ini
> Copying .bandit
> Copying tests/__init__.py
> Copying src/__init__.py
> Renaming src to templ8
> Running python -m venv venv --without-pip
```

### Plugins

All collection sources contain a specification file at their root.

**`metadata.json`**:

```json
{
  "default_variables": {
    "classifiers": [],
    "console_scripts": [],
    "tox_envlist": ["py36", "py37", "py38"],
    "travis_test_envlist": ["3.6", "3.7", "3.8"],
    "install_requires": [],
    "keywords": [],
    "pytest_ignore_glob": null,
    "python_requires": 3.6
  },
  "dynamic_folders": { "src": "package_name" },
  "initialization": ["python -m venv venv --without-pip"]
}
```

## Tests

To run unit tests and generate a coverage report:

```bash
grunt tests:unit
```

## Documentation

This repository's documentation is hosted on [readthedocs][readthedocs].

To generate the sphinx configuration:

```bash
grunt docs:generate
```

Then build the documentation:

```bash
grunt docs:build
```

## Tooling

To run linters:

```bash
grunt lint
```

To run formatters:

```bash
grunt format
```

Before committing new code:

```bash
grunt precommit
```

This will run linters, formatters, tests, generate a test coverage report and the sphinx configuration.

## Continuous integration

This repository uses Travis CI to build and test each commit. Formatting tasks and writing/generating documentation must be done before committing new code.

## Versioning

This repository adheres to semantic versioning standards.
For more information on semantic versioning visit [SemVer][semver].

Bump2version is used to version and tag changes.
For example:

```bash
bump2version patch
```

## Changelog

Please read this repository's [CHANGELOG](CHANGELOG.md) for details on changes that have been made.

## Contributing

Please read this repository's guidelines on [CONTRIBUTING](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Contributors

- **Joel Lefkowitz** - _Initial work_ - [Joel Lefkowitz][author]

[![Buy Me A Coffee][coffee_button]][coffee]

## Remarks

Lots of love to the open source community!

![Be kind][be_kind]

<!-- Public links -->

[semver]: http://semver.org/

<!-- External links -->

[readthedocs]: https://templ8.readthedocs.io/en/latest/
[coffee]: https://www.buymeacoffee.com/joellefkowitz
[coffee_button]: https://cdn.buymeacoffee.com/buttons/default-blue.png
[be_kind]: https://media.giphy.com/media/osAcIGTSyeovPq6Xph/giphy.gif

<!-- Acknowledgments -->

[author]: https://github.com/joellefkowitz

<!-- Project shields -->

[release_shield]: https://img.shields.io/github/v/tag/joellefkowitz/templ8
[license_shield]: https://img.shields.io/github/license/joellefkowitz/templ8
[lines_shield]: https://img.shields.io/tokei/lines/github/joellefkowitz/templ8
[languages_shield]: https://img.shields.io/github/languages/count/joellefkowitz/templ8

<!-- Health shields -->

[codacy_shield]: https://img.shields.io/codacy/grade/f407d8c4db8c4b83877bca0543aba744
[readthedocs_shield]: https://img.shields.io/readthedocs/templ8
[travis_shield]: https://img.shields.io/travis/com/joellefkowitz/templ8
[codacy_coverage_shield]: https://img.shields.io/codacy/coverage/f407d8c4db8c4b83877bca0543aba744

<!-- Repository shields -->

[issues_shield]: https://img.shields.io/github/issues/joellefkowitz/templ8
[issues_closed_shield]: https://img.shields.io/github/issues-closed/joellefkowitz/templ8
[pulls_shield]: https://img.shields.io/github/issues-pr/joellefkowitz/templ8
[pulls_closed_shield]: https://img.shields.io/github/issues-pr-closed/joellefkowitz/templ8

<!-- Publishers shields -->

[pypi_shield]: https://img.shields.io/pypi/v/templ8
[python_versions_shield]: https://img.shields.io/pypi/pyversions/templ8
[pypi_downloads_shield]: https://img.shields.io/pypi/dw/templ8

<!-- Activity shields -->

[contributors_shield]: https://img.shields.io/github/contributors/joellefkowitz/templ8
[monthly_commits_shield]: https://img.shields.io/github/commit-activity/m/joellefkowitz/templ8
[last_commit_shield]: https://img.shields.io/github/last-commit/joellefkowitz/templ8
