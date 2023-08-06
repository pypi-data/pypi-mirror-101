f2r
===

Command line tool to create RPMs out of aliBuild output

## Installation

`f2r` is available in PyPI: https://pypi.org/project/f2r

Steps:
- Use `f2r` Ansible role from [system-configration](https://gitlab.cern.ch/AliceO2Group/system-configuration).
- Create S3 config file under `~/.s3cfg`, see: https://gitlab.cern.ch/AliceO2Group/system-configuration


## Devel

#### Devel installation

- Instll prerequisites
  - Environment Modules > 4
  - aliBuild
  - Optional install system dependencies that aliBuild can pick up
- Clone the repo
- Prepare S3 config
- `python3 -m pip install -r requirements.txt --user`

#### Publishing to PyPI
- Update version in `setup.py` file.
- Test: `python3 -m tests.f2r`
- Build and publish:
```
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository pypi dist/*
```
