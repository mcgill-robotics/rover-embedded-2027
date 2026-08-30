
# Installing the rover-embedded package

This document will explain various installation scenarios for this package

## Table of contents
- [Installing the rover-embedded package](#installing-the-rover-embedded-package)
	- [Table of contents](#table-of-contents)
	- [Default installation](#default-installation)
	- [Installing Offline](#installing-offline)
	- [Optional Features](#optional-features)
	- [Editable Install](#editable-install)
	- [Bonus: Using uv](#bonus-using-uv)


## Default installation

 To install the `rover-embedded` Python package with `pip`, run the following command:

```sh
pip install <path to package>
```

where `<path to package>` would be `./bridge` from the root of the `rover-embedded-2027` 
repository or `.` from the directory where this `INSTALL.md` file is located.

**Example install command**

```sh
pip install ./bridge
```

Once that is done, the code in the package may be imported by any python script in the following way.


```py
from rover_embedded.comms import pantilt_firmware

# Your code continues here...
```

## Installing Offline

If you need to install offline, build and runtime dependencies will need to be manually installed to the environment you plan to run the scripts from. 

Currently, the only build time dependency is `hatchling >= 1.26` which is used
as the build backend. Always check the [pyproject.toml](./pyproject.toml) file for the most up to date list of dependencies.

> ℹ️ The build time dependencies can be found in the `build-system` section.
> Runtime dependencies can be found under the `dependencies` key of the `project` section or under `project.optional-dependencies` for optional ones.

Once everything has been pre-downloaded, the environment can be used to build and install the package by using the following command:

```sh
pip install <path to package> --no-build-isolation
```

See the [Default Installation](#default-installation) section for more about what to use for the path.

> ℹ️ `--no-build-isolation` is required because pip used an isolated environment for builds by default which causes dependencies to be downloaded. 
> `--no-build-isolation` allows the use of the existing environment where all dependencies including the build time ones have been preinstalled. Learn more at https://pip.pypa.io/en/stable/reference/build-system/#build-isolation

## Optional Features

Some features of the package may require additional dependencies that are not 
installed by the default install method. To get those additional features use the following command.

```sh
pip install <path to package>[<extra name>]
```

where `<extra name>` refers to a group of optional dependencies. 

Currently, there are available extras in this package, `gui` and `all`. The `all` extra will download all optional dependencies available (right now this is the same as `gui`). `gui` contains dependencies for running web ui.

**Example install command**

```sh
pip install ./bridge[gui]
```

## Editable Install

If you require installing once but want to be able to change files in the package without reinstalling a new version, the package can be installed as an editable install using the following command:

```sh
pip install -e <path to package>
```

## Bonus: Using uv

All the previous sections can also be done with equivalent `uv` commands if you 
use `uv` to manage your project.

**Default**

```sh
uv add <path to package> 
```
**Offline install**

```sh
uv add --no-build-isolation <path to package>
```

**Optional Features**

```sh
uv add <path to package> --group <extra name>
```

**Editable**

```sh
uv add --editable <path to package> 
```