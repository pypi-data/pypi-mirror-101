===================================================
Additional PostgreSQL database functions for Django
===================================================


About
=====
This extension adds some PostgreSQL database functions.

Installation
============

You can install django_postgresql_function either via the Python Package Index (PyPI)
or from source.

To install using `pip`,:

.. code-block:: console

    $ pip install -U django_postgresql_function

Usage
=====

To use this with your project you need to follow these steps:

#. Install the django_postgresql_function library:

   .. code-block:: console

      $ pip install django_postgresql_function

#. Add ``django_postgresql_function`` to ``INSTALLED_APPS`` in your
   Django project's ``settings.py``::

    INSTALLED_APPS = (
        ...,
        'django_postgresql_function',
    )

   Note that there is no dash in the module name, only underscores.