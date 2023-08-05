castaway
========

.. image:: https://github.com/dakrauth/castaway/workflows/Test/badge.svg
   :target: https://github.com/dakrauth/castaway/actions
   :alt: GitHub Actions

A simple wrapper for python-dotenv_ that allows for easy casting of environment
strings to various data types.

.. _python-dotenv: https://pypi.org/project/python-dotenv/

Installation
------------

Standard install:

.. code::

    pip install castaway


If you want Django integration (``dj-email-url``, ``dj-database-url``), do:

.. code::

    pip install castaway[django]


Example
-------

Easiest form is:

.. code:: python

    from castaway import config
    SOME_SETTING = config('SOME_SETTING', default=None)

Like ``python-dotenv``, this will load ``.env`` from the current working directory,
or walk the parent directory tree until it is found.

For more custom usage, you can specify the exact name and path to whatever file you need.
For instance, using the ``tests/.env`` file from this repo.

.. code:: python

    from datetime import datetime
    from castaway import Config

    config = Config('tests/.env')

    CASTAWAY_INT = config('CASTAWAY_INT', cast=int)
    assert CASTAWAY_INT == 23

    CASTAWAY_LIST = config('CASTAWAY_LIST', cast=list)
    assert CASTAWAY_LIST == ['a', 'b', 'c']

    CASTAWAY_DATETIME = config('CASTAWAY_DATETIME', cast=datetime.fromisoformat)
    assert CASTAWAY_DATETIME == datetime(2021, 4, 3, 14, 25)
