##############################################################################
django-keys 1.0.1
##############################################################################

Python package and CLI tool for generating and handling secret keys used by
Django applications.

This Python module is used to generate and handle secret keys for Django:

* read Django's `SECRET_KEY` from file that is kept out of version control
* don't need to manage secret key outside of production
* features a CLI tool to generate secret keys for Django


===============================================================================
Retrieve `SECRET_KEY` From File
===============================================================================

`django-keys` provides the function `retrieve_secret_from_file()` for reading
Django's `SECRET_KEY` from a file that can be kept out of version control. By
adding the following line, we do not have to worry about managing our secret
key outside of production.

.. code-block :: python

    import djangokeys

    SECRET_KEY = djangokeys.retrieve_secret_key_from_file("secret.key", strict=(not DEBUG))

When the strict parameter is set to `True`, it is required that the file
exists. If it cannot be found, an exception is raised. However, if strict is
set to False, a file is generated with a new secret key.


==============================================================================
CLI Tool
==============================================================================

This module also features a CLI tool that can be used to generate secret
keys for Django.

For more information, use the following command:

.. code-block :: sh

    $ python3 -m djangokeys --help


You can generate a new key and store it in the file `secret.key` by using the
command below:

.. code-block :: sh

    $ python3 -m djangokeys --length 128 > secret.key


==============================================================================
Install
==============================================================================

You can install this package using pip:

.. code-block:: sh

    $ pip install --user django-keys


==============================================================================
License
==============================================================================

This project is released under the MIT license.

