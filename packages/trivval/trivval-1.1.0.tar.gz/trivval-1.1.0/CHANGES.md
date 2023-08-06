# Changelog for trivval, the trivial data structure validation library

## 1.1.0 (2021-04-07)

- Allow an optional key to be present with a null value.

## 1.0.2 (2021-03-31)

- Add Python 3.9 as a supported version.
- Add a PEP 517 build framework.
- Drop the outdated pylintrc file.
- Add a manifest file for the source distribution.
- Move some tool configuration options to setup.py and pyproject.toml.
- Rename some of the tox environments.
- Push the source down into a src/ directory.
- Drop the unit-tests-bare tox environment.
- Add a mypy stub file for pytest.
- Go back to using packaging instead of the deprecated distutils.

## 1.0.1 (2020-09-06)

- Reformat the source code using black 20.
- Use distutils.version instead of packaging.version.
- Use super() with no arguments we depend on Python 3.x.
- Propagate a ValidationError's traceback information when
  reraising it in an outer scope.

## 1.0.0 (2020-04-14)

- Only support Python 3.6 or later:
  - drop the Python 2.x unit tests and mypy check
  - unconditionally import typing and pathlib
  - drop the "equivalent types" support only needed for
    the Python 2.x `unicode`/`str` weirdness
  - no longer inherit from `object`
  - use f-strings for errors and diagnostic messages
  - use Python 3.x's `unittest.mock` and drop `fake_mock`
- Use the `mistune` library to validate the Markdown files.

## 0.1.0 (2020-04-14)

- First public release.
