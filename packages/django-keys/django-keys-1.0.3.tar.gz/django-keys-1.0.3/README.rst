##############################################################################
django-keys 1.0.3
##############################################################################

.. image:: https://travis-ci.com/alanverresen/django-keys.svg?branch=master
    :target: https://travis-ci.com/alanverresen/django-keys
    :alt:

.. image:: https://readthedocs.org/projects/django-keys/badge/?version=latest
    :target: https://django-keys.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

**django-keys** is a Python 3 package and CLI tool that can be used for
handling the secret keys and other settings of Django projects securely. It
allows you to specify the settings of your Django project in two ways:

* using environment variables set by execution environment
* using a local .env file containing key-value pairs

The configuration of a Django project typically varies based on its deployment
environment (development, production, testing, ...). This hybrid approach
makes it easy to specify and manage the settings per environment, regardless of
the execution environment and the tools that are used.


===============================================================================
Basic Usage
===============================================================================

During development, we can specify the settings used by our Django project in a
local '.env' file, so that we do not have to alter the environment variables
of our dev machine. **This file should be kept out of version control, as it
may contain sensitive information!**

.. code-block:: sh

   # .env file
   EMAIL_HOST=example.org
   EMAIL_PORT=587
   EMAIL_USER=user@example.org
   EMAIL_PASSWORD=password123
   EMAIL_TLS=true
   SECRET_KEY=secret123
   ...

After specifying the settings that we will use during development in our
local `.env` file, we should import the `djangokeys` module, and create an
instance of the `DjangoKeys` class in Django's settings file. It will load
all environment variables from our local `.env` file, or the environment
variables set by the execution environment, our local dev machine.

.. code-block:: python

   # initialize your DjangoKeys instance
   from djangokeys import DjangoKeys
   keys = DjangoKeys("/path/to/.env")

   # automatically convert environment variables to the right type
   EMAIL_HOST = keys.str("EMAIL_HOST")
   EMAIL_PORT = keys.int("EMAIL_PORT")
   EMAIL_ADDRESS = keys.str("EMAIL_ADDRESS")
   EMAIL_PASSWORD = keys.str("EMAIL_PASSWORD")
   EMAIL_USE_TLS = keys.bool("EMAIL_USE_TLS")

   # use the .secret_key method to access your secret key
   SECRET_KEY = keys.secret_key("SECRET_KEY")

   # check for any potential problems
   keys.report_problems()


When we later try to test, deploy, ... our Django project, we can specify the
settings for that execution environment using environment variables in a
Dockerfile, via Travis' web interface, ... instead of having to create a local
`.env` file. When the local `.env` file doesn't exist, the program continuous,
assuming that all environment variables have been set by the execution
environment.


===============================================================================
CLI Tool
===============================================================================

This package also features a convenient commandline interface tool that can be
used to generate secret keys for Django, or automatically create a new `.env`
file based on Django's setting module.

For more information, use the following command:

.. code-block:: sh

    $ python3 -m djangokeys --help


You can generate a new key by using the `generate-key` action:

.. code-block:: sh

    $ python3 -m djangokeys generate-key --length 128

After integrating `django-keys` into Django's settings module, you can also
automatically generate a new .env file with all used environment variables:

.. code-block:: sh

    $ python3 -m djangokeys generate-env --settings 'config.settings'


The `.env` file will be generated at the location specified in the settings
file. It will automatically generate a new secret key, if the `secret_key()`
method is used in your settings file to access the environment variable.

**IMPORTANT: The `generate-env` action hasn't been implemented yet.**


==============================================================================
Install
==============================================================================

This package is currently available for Python 3.7 and up.
You can install this package using pip:

.. code-block:: sh

    $ pip install --user django-keys


==============================================================================
License
==============================================================================

This project is released under the MIT license.
