# gada-pyrunner

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gada-pyrunner)
[![Python package](https://img.shields.io/github/workflow/status/gadalang/gada-pyrunner/Python%20package)](https://github.com/gadalang/gada-pyrunner/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/gada-pyrunner/badge/?version=latest)](https://gada-pyrunner.readthedocs.io/en/latest/?badge=latest)
[![Codecov](https://img.shields.io/codecov/c/gh/gadalang/gada-pyrunner?token=4CSJTL1ZML)](https://codecov.io/gh/gadalang/gada-pyrunner)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/gadalang/gada-pyrunner/issues)

Python runner for [gada](https://github.com/gadalang/gada).

## Install

Using pip:

```bash
$ pip3 install gada-pyrunner
```

## Documentation

Build the doc with:

```bash
$ make html
```

You can find the latest documentation on [gada-pyrunner.readthedocs.io](https://gada-pyrunner.readthedocs.io/).

## Basic example

Create a Python package with the following structure and add it to your `PYTHONPATH`:

```bash
├── mycomponent
│   ├── __init__.py
│   ├── mynode.py
│   └── config.yml
```

Content of `mynode.py`:

```python
def main():
    print("hello world")

if __name__ == "__main__":
    main()
```

Content of `config.yml`:

```yaml
nodes:
  mynode:
    runner: python
    file: ${comp_dir}/mynode.py
```

Usage:

```bash
$ gada mycomponent.mynode
hello world
```

## Testing

The `test` directory contains many tests that you can run with:

```python
$ tox .
```

## License

Licensed under the [MIT](LICENSE) License.
