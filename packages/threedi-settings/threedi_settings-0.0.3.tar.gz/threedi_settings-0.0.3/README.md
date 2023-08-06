## threedi-settings


Convert legacy model ini settings files to API V3 resources.


### Installation

To get all functionalities this package as to offer, install with all extras

    $ pip install threedi-settings[cmd, api]

### Usage

Ths will give you access to the command line interface that let's you convert 3Di model settings to
3Di API resources like so

    $ import_simulation_setings <simulation id> <path to model ini file>

The example above requires a `simulation_id` argument as settings can be defined
on a per simulation basis in the API. That gives you much more flexibility to experiment
with different configurations.


### Internal Usage

This package is also used to retrieve simulation settings resources from the API to further
convert them to an internal format that the 3Di calculation core is able to read and process.

The package therefore can be installed without the extras mentioned above or a
single extra like `api` which will give you the `threedi-api-client` requirement
and therefore access to the http module.


* Free software: MIT license
* Documentation: https://threedi-settings.readthedocs.io.



#### Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.

