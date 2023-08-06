# GetFX

GetFX is a tool to download average FX rates from National Bank of Poland (NBP). All NBP exchange rates are to Polish Złoty (PLN).

| Check        	   | Result        |
| -------------    |:------------:|
| Build            | ![](https://github.com/kniklas/get-fx/workflows/build/badge.svg)|
| Coverage (master)| [![Coverage Status](https://coveralls.io/repos/github/kniklas/get-fx/badge.svg?branch=master&t=xgdvqo)](https://coveralls.io/github/kniklas/get-fx?branch=master)|
| Coverage (dev)   | [![Coverage Status](https://coveralls.io/repos/github/kniklas/get-fx/badge.svg?branch=dev&t=xgdvqo)](https://coveralls.io/github/kniklas/get-fx?branch=dev)|

# Installation

Pre-requisites to install GetFX:
* [pip](https://pip.pypa.io/en/stable/installing/) 
* [setuptools](https://pypi.org/project/setuptools/)

Typically above applications are installed by default when you install python from [python.org](https://www.python.org).

Alternatively you can install GetFX from this repository source code. After you clone the repository execute from shell: `make build`.


# Usage

You can use the package from command line (example using Linux or MacOS):
* `getfx` - will return today FX from default currency (CHF)
* `getfx USD` - will return today FX for USD
* `getfx USD -d 2020-10-03` - will return USD FX on 3th October 2020
* `getfx -h` - display help

Eventually you can run package using `python3` command:
* `python3 -m getfx` - same as first example above
* `python3 -m getfx USD` - same as second example above
