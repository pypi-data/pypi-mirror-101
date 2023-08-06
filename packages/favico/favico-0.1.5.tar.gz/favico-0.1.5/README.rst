===============================
favico
===============================

.. image:: https://github.com/romnn/favico/workflows/test/badge.svg
        :target: https://github.com/romnn/favico/actions
        :alt: Build Status

.. image:: https://img.shields.io/pypi/v/favico.svg
        :target: https://pypi.python.org/pypi/favico
        :alt: PyPI version

.. image:: https://img.shields.io/github/license/romnn/favico
        :target: https://github.com/romnn/favico
        :alt: License

.. image:: https://codecov.io/gh/romnn/favico/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/romnn/favico
        :alt: Test Coverage

""""""""

Python library to generate the perfect favicons for every device.

.. code-block:: console

    $ pip install favico

.. code-block:: python

    import favico

Installation
-------------

favico uses `ImageMagick <https://imagemagick.org/index.php>`_ to generate the favicons.

For ubuntu, you can simply install libmagicwand-dev like this:

.. code-block: console

    $ apt-get install libmagickwand-dev 

Development
-----------

For detailed instructions see `CONTRIBUTING <CONTRIBUTING.rst>`_.

Tests
~~~~~~~
You can run tests with

.. code-block:: console

    $ invoke test
    $ invoke test --min-coverage=90     # Fail when code coverage is below 90%
    $ invoke type-check                 # Run mypy type checks

Linting and formatting
~~~~~~~~~~~~~~~~~~~~~~~~
Lint and format the code with

.. code-block:: console

    $ invoke format
    $ invoke lint

All of this happens when you run ``invoke pre-commit``.

Note
-----

This project is still in the alpha stage and should not be considered production ready.
